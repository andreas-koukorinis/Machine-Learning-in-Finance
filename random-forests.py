#Python program to find k-NN to predict returns on stocks
#Author: Vishal Surana
#Python version 3.1, tested using IDLE on Windows

import random
import operator
from math import sqrt

def transform(num,index):
        if(index==0):
                return (float(num)/500)
        if(index==1):
                return (float(num)/1000)
        if(index==2):
                return 1.0*(((float(num)-0.5)/2.5))
        if(index==3):
                return 10*(float(num))
        if(index==4):
                return float(num)
       

def readfile(filename,rows,cols,nclasses):
    fopen=open(filename)
    i=0
    X=[[0.0 for _ in range(cols)] for _ in range(rows)]
    for line in fopen.readlines():
        j=0
        #number=0
        data=line.split(',')
        for item in data:
            X[i][j]=transform(item,j)
            j=j+1
        #print (X[i])
        X[i][cols-1]=nclasses-0.4*nclasses/(X[i][4]+0.2)
        i=i+1
    fopen.close()    
    return X
       

def results(testdata,f):
    global table
    i=0
    ntest=len(testdata)
    dim=len(testdata[0])
    l1=[0]*dim
    #f=[0]*ntest
    for item in testdata:
        cur=0
        search=1
        #print l1
        while(search and cur>=0):
            #print cur,q,l1
            l1=table[cur]
            if(l1[3]==-1):
                search=0
                f[i]=f[i]+l1[1]
                #print i,f[i]
            else:
                if(item[l1[0]]<=l1[1]):
                    cur=l1[2]
                else:
                    cur=l1[3]
        i=i+1
    return f
       

def statistics(ntrees,testdata,f):
    error=0.0
    i=0
    #print f
    for data in testdata:
        f[i]=f[i]/ntrees
        #if(f[i]*traindata[i][4]<0):    #error in predicting even the direction
        #    print f[i], data[4],"\n"
        error=error+abs(f[i]-data[4])
        i=i+1
    ntest=i
    print "Number of Test Points=",ntest,"\n"
    print "Average Error=",error/ntest,"\n"


####################################
#    Initialize basic parameters   #
random.seed()
nclasses=5
dim=6
ntrain=1000
ntest=200
ntrees=100
itermax=10
maxnodes=20000
features=range(dim-1)
####################################

#read data
traindata=readfile("train.csv",ntrain,dim,nclasses)    
testdata=readfile("test.csv",ntest,dim,nclasses)

#Modify this single line to use some other data for testing
testingdata=testdata
f=[0]*len(testingdata)

#Build the decision tree(stored as a table)
for q in range(ntrees):
    tab=open("table.csv","w");  #Debug Output
    roots=range(maxnodes,0,-1)     #Data structure to ensure that that the ith row corresponds to ith node
    temp=[0, range(ntrain)]     
    #print temp,len(temp)
    table=[];                   #New tree for each iteration
    entry=[]
    while len(temp)>0:
        #r=random.randint(0,len(features))      #without replacement
        r=random.randint(0,dim-2)               #with replacement
        feature=features[r]
        pid=temp.pop(0)
        children=temp.pop(0)
        mmax=len(children)
        #print "children=", children

        j=0
        diff=1
        while (diff and j<itermax):             #If we cannot find a pair after itermax iterations, then club them all in a terminal node
                p1=children[random.randint(0,mmax-1)]
                p2=children[random.randint(0,mmax-1)]
                if(traindata[p1][dim-1]!=traindata[p2][dim-1]):
                   diff=0
                   break
                j=j+1
    
        if(diff==0):
       
            alpha=random.uniform(0,1)
            split=alpha*traindata[p1][feature]+(1-alpha)*traindata[p2][feature]
            #print split

            l1=[]
            l2=[]
            for item in children:
                #print traindata[item][feature]
                if(traindata[item][feature]<=split):
                    #print "yes"
                    l1.append(item)
                else:
                    #print "no"
                    l2.append(item)
            if(len(l1)<mmax and len(l1)>0):   #both sides have at least one element
                #print i1
                r1=roots.pop()
                r2=roots.pop()
                entry=[feature, split, r1, r2]
                #print entry, "\n"
                temp.extend([r1, l1, r2, l2])
                diff=-1
        if(diff!=-1):
            #print "Terminal Node Found"
            tot=0
            for item in children:
                tot=tot+traindata[item][4]
            entry=[feature, tot/mmax, -1, -1]
        #print entry, "\n"
            
        table.append(entry)
        s = str(entry)
        s = s.replace("[", "")
        s = s.replace("]", "")
        tab.write(s+"\n")
    #print table,"\n"
    tab.close()
    rows=len(table)
    print rows,"\n"
    
    f=results(testingdata,f)

#Find the final predicted values, overall error
statistics(ntrees,testingdata,f)
