'''
Created on Apr 25, 2010

@author: vishal
'''
#import sys
#sys.path.append('./')
from csvapi import StockPriceData
import sys

if __name__ == "__main__":
    
    data=StockPriceData("./")
    # returns the list of valid stocks from user input
    stocks = data.getStocksList('./stocks.txt')
    print data
    startDate = 20070101
    endDate = 20100101
    if(endDate<startDate):
        print "Error: enddate earlier than startdate"
        sys.exit(0)
    
    timestamps = data.getTimeStamp(startDate,endDate) # returns the list of timestamps
    print timestamps
    data.getData(stocks,timestamps) #creates the array
   
    for i in range(len(timestamps)): 
        for j in range(len(stocks)): 
            if data.priceArray[i][j] == NaN:  
                data.priceArray[i][j] = data.priceArray[i][j-1]
                print i, j
            else:
                print 'vishal'
            #elif (j>0 & data.priceArray[i][j] < 1.0 & data.priceArray[i][j-1]>=1):
                
            

    '''
    print data.priceArray[0][0]
    print(data.priceArray[len(timestamps)-1][len(stocks)-1])
    print "ts="+str(len(timestamps))+"stocks="+str(len(stocks))
    print(data.priceArray[755][131])
    '''
