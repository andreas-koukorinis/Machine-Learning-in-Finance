#Python program to find k-NN for return on stocks
#Author: Vishal Surana
#Python version 3.1, tested using IDLE on Windows

import operator

i=0
X=[[0.0 for _ in range(5)] for _ in range(1000)]
Z=[0.0 for _ in range(5)]
R=[]
dot=[]
Y=[]
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


test=open("test.csv");
output=open("yprime.csv","w")
l=0
total=0
rad = 10
for line in test.readlines():
    j=0
    data=line.split(',')

    Z=[]
    for item in data:
        Z.append(float(item))
            #print(Z[j]);
            #j=j+1
    #print(Z)
#########################################################
#     This method works only for equal weights          #
#########################################################

    pred = 0
    pred2 = 0
    nelem = 0
    closest = 100000
    for k in range(0,i):
        number=R[k]-2*(Z[0]*X[k][0]+Z[1]*X[k][1]+Z[2]*X[k][2]+Z[3]*X[k][3])
        if number<rad:
            pred = pred + X[k][4]
            nelem = nelem + 1
        elif number<closest:
            closest = number
            pred2 = X[k][4]

    if nelem>0:
        pred = pred/nelem
    else:
        pred = pred2

    error=abs(pred-Z[4])
    #print(pred,Z[4])
    temp=str(error)+"\n"
    output.write(temp);
    dot=[]
    #print(len(dot))
    total=total+error
    l=l+1
    #print(len(R))
print ("Average Error=",total/l,"\n");

