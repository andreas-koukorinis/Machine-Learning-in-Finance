#Python program to find first 100 primes
#Author: Vishal Surana
#Python version 3.1, tested using IDLE on Windows
from math import sqrt
import operator
#from numeric import zeros
#read training data from file
i=0
X=[[0.0 for _ in range(5)] for _ in range(1000)]
Z=[[0.0 for _ in range(4)] for _ in range(1000)]
R=[]
dot=[]
Y=[]
#X=zeros([4,1000],Float);
print (R)
#Z=[0.0,0.0,0.0,0.0,0.0]*1000
#R=[0.0]*1000
#dot=[0.0,0.0]*1000
train=open("train.csv");
for line in train.readlines():
        j=0
        number=0
        data=line.split(',')
        for item in data:
                X[i][j]=float(item)
                j=j+1
                if(j<4):
                        number=number+float(item)*float(item)
                R.append(number)
        i=i+1
	#print (number)

test=open("test.csv");
l=0
total=0
for line in test.readlines():      
        j=0
        data=line.split(',')
        for item in data:
                Z[j]=float(item)
                j=j+1
        for k in range(0,i):
                number=R[k]-2*(Z[0]*X[k][0]+Z[1]*X[k][1]+Z[2]*X[k][2]+Z[3]*X[k][3])
                dot.append([number,X[k][4]])
                #print (dot[k])
        Y.append(Z[4])
        sorted(dot,key=operator.itemgetter(0))
        pred=(dot[0][1]+dot[1][1]+dot[2][1]+dot[3][1])/4
        error=abs(pred-Z[4])
        total=total+error
        l=l+1
print ("Average Error=",total/l,"\n");

#########################################################
#This method works only for equal weights               #
#########################################################



