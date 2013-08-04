import dircache, time
from sets import Set as set
from numpy import NaN
import sys
import numpy as np
value = NaN


##	This file contains a collection of APIs to easily grab data from CSV files containing real price data
##
##	The Class is StockPriceData and it takes as argument the path to the folder conatining all the CSVs.
##
##	The APIs are listed below. 
##


class StockPriceData:
    def __init__(self,dirname):
        self.dirname=dirname
        self.list_user_file_names = []
        self.filt_list=[]
        self.startDate = 0
        self.endDate= 0
        self.count_of_non_existent_stocks = 0
        self.priceArray = np.ndarray( shape=(0,0), dtype=np.object)
        self.stocks_list = []
        


##
##  1)	getSymbols() - Returns all the available symbols in allcsv directory [the folder which contains all the CSV files] directory.
##	The path to the folder which is passed when creating an object for the class is used. 
##

#used to get the symbols from the allcsv directory
    def getSymbols(self):
        list_file_names=dircache.listdir(self.dirname)
        list_file_names_strip_txt = map(lambda x:(x.split('.')[0]),list_file_names)
        return list_file_names
        # print list_file_names_strip_txt

##
## 2) getStocksList(filename) - Takes as input a list of ticker symbols and returns as output a list of valid available stocks.
##
##	This method uses two other methods getUserSymbols() and getMySymbols.
##
##	getStocksList(filename) - This method would return a list of all the stocks that were valid and for which data is available in the allcsv directory
##	getMySymbols() - This method returns the list of valid tickers which is available in the allcsv directory.
##	getUserSymbols() - This method is used to collect the user ticker symbols.
##
##
##

# to get the user specified symbols       
    def getUserSymbols(self,filename):
        f=open(filename)
        list_user_tickers=f.readlines()
        f.close()
        for i in range(0,len(list_user_tickers)):
            list_user_tickers[i]=list_user_tickers[i].strip()
            #stocks_list.append(list_user_tickers[i].upper())
            list_user_tickers[i]=str(list_user_tickers[i]).upper()+".TXT"
            # print "user_tickers" + str(list_user_tickers)
        return list_user_tickers

# to find intersection of user specified symbols and allsymbols to leave out type etc
    def getMySymbols(self,filename):
        a=Set(self.getSymbols())
        b=Set(self.getUserSymbols(filename))
        c=a.intersection(b)
        list_user_file_names=list(c)
        list_user_file_names.sort()
        self.list_user_file_names = list_user_file_names
        list_user_file_names_strip_txt = map(lambda x:(x.split('.')[0]),list_user_file_names)
        #print "strip_txt" + str(list_user_file_names_strip_txt)
        return self.list_user_file_names


#get the stock list
    def getStocksList(self,filename):
        sym=self.getMySymbols(filename)
        self.stocks_list = map(lambda x:(x.split('.')[0]),sym)
        #print "stocks_list" + str(stocks_list)
        return self.stocks_list


##
## 3) getCalendar(symbol) - This method takes as input a symbol and returns as output all days the given symbol has traded.
##



#used to get all the dates a particular stock has been traded
    def getCalendar(self,symbol):
        symbol = str(symbol).upper() + ".TXT"
        f=open(str(self.dirname)+"/"+str(symbol))
        j=f.readlines()
        f.close()
        j=j[1:-1]
        stock_trading_days=map(lambda x:(x.split(',')[1]),j)
        #print stock_trading_days
        return stock_trading_days


## # 4) getTimeStamp(symbol) - This method takes as input the start date and end
#date and returns as output the trading days within the maximum range of oldest
#stock in the user input. So for example if you want to see the trading
#days from 1970 to 2009 with symbols of aapl, goog and yhoo. it would
#return the trading days from 1982(when aapl went public) till 2009. 
#This method in turn uses constructFilteredList() method and data from getMySymbol. 
##


#get the time stamp
    def getTimeStamp(self,startDate,endDate):
        self.constructFilteredList(startDate,endDate)
        date_sorted = []
        for i in range(0,len(self.filt_list)):
            date_sorted.append(int(self.filt_list[i][0][1]))
            

        csv_date = -1     
        for i in range(0,len(date_sorted)):
            if(min(date_sorted)==date_sorted[i]):
                csv_date = i
                break
       
        timestamp_list = []
        if(csv_date!=-1):
            for i in range(0,len(self.filt_list[csv_date])):
                temp=[]
                temp.append(self.filt_list[csv_date][i][1])
                timestamp_list.append(temp)        
                # print timestamp_list

        timestamp_list = map(lambda x: x[0],timestamp_list)
        return timestamp_list
        
# get an intermediate list (which is required by all classes-to make the extraction faster)           
    def constructFilteredList(self,startDate,endDate):
        self.startDate = startDate
        self.endDate = endDate
        user_file_names_extract_data=self.list_user_file_names
               
        
        for x in user_file_names_extract_data:
            f=open(str(self.dirname)+"/"+str(x)) # Change the directory structure according to your Operating System eg: '/' for linux
            j=f.readlines()
            f.close()
            j=j[1:-1]
            filt_list_temp=filter(lambda x: (int(x.split(',')[1])> int(self.startDate)) ,j)
            filt_list_temp=filter(lambda x: (int(x.split(',')[1])< int(self.endDate)) ,filt_list_temp)
            if filt_list_temp:
                filt_list_temp=map(lambda x:(x.split(',')[0],x.split(',')[1],x.split(',')[2],x.split(',')[3],x.split(',')[4],x.split(',')[5],x.split(',')[6],(x.split(',')[7]).strip()),filt_list_temp)
                self.filt_list.append(filt_list_temp)
            else:
                # self.count_of_non_existent_stocks = self.count_of_non_existent_stocks + 1
                print str(x.split('.')[0]) + " didn't exist in this period\n"
                self.stocks_list.remove(x.split('.')[0])
        return self.filt_list


##
## 5) getData(listofstocks,listoftimestamps) - Returns the data in a numpy ndarray with dimensions -> timestamps as rows and stocks as columns.
##					    Uses data returned from getTimestamp and getStocksList.
##
##					  - Currently this method creates an array with each cell constituting a dictionary containing the following values
##					    adj_close, adj_open, volume, timestamp, exchange, adj_high, adj_low and others. But this could be modified for just 					    having the just the adjusted closing price for instance. eg: self.priceArray[j,i] = self.filt_list[i][k][5]
##					
##
##


#build the array
    def getData(self,stocks_list,timestamp_list):
        timestamps = np.array(timestamp_list)
        stocks = np.array(stocks_list)
        self.priceArray = np.ndarray( shape=(timestamps.size, stocks.size), dtype=np.object)

       
        for i in range(stocks.size): # - self.count_of_non_existent_stocks):
            #  print str(stocks[i]) + str(len(self.filt_list[i])) + "i= " + str(i)
            k = 0
            for j in range(timestamps.size):
                if(k<len(self.filt_list[i])):
                    #print str(timestamps[j]) +" befor<= "+ str(self.filt_list[i][k][1]) +" "+ str(i) +" "+ str(j) +  " "+ str(k)
                    if(timestamps[j]<self.filt_list[i][k][1]):
                        #   print str(timestamps[j]) +" < "+ str(self.filt_list[i][k][1]) +" "+ str(i) +" "+ str(j) +  " "+ str(k)
                        row = {}
                        row['exchange'] = 'NYSE'
                        row['symbol'] = self.filt_list[i][k][0]
                        row['adj_open'] = NaN 
                        row['adj_close'] = NaN
                        row['adj_high'] = NaN
                        row['adj_low'] = NaN
                        row['close'] = NaN
                        row['volume'] = NaN
                        parseddate = time.strptime(timestamps[j],'%Y%m%d')
                        row['timestamp'] = timestamps[j]
                        row['when_available'] = time.mktime(parseddate)
                        row['interval'] = 86400
                        self.priceArray[j,i] = row
                    elif(timestamps[j]==self.filt_list[i][k][1]):
                        #  print str(timestamps[j]) +" == "+ str(self.filt_list[i][k][1]) +" "+ str(i) +" "+ str(j) +  " "+ str(k)
                        row = {}
                        row['exchange'] = 'NASDAQ'
                        row['symbol'] = self.filt_list[i][k][0]
                        row['adj_open'] = self.filt_list[i][k][2] 
                        row['adj_close'] = self.filt_list[i][k][5]
                        row['adj_high'] = self.filt_list[i][k][3]
                        row['adj_low'] = self.filt_list[i][k][4]
                        row['close'] = self.filt_list[i][k][7]
                        row['volume'] = self.filt_list[i][k][6]
                        parseddate = time.strptime(timestamps[j],'%Y%m%d')
                        row['timestamp'] = timestamps[j]
                        row['when_available'] = time.mktime(parseddate)
                        row['interval'] = 86400
                        self.priceArray[j,i] = row
                        k=k+1
                else:
                    row = {}
                    row['exchange'] = 'NYSE'
                    row['symbol'] = self.filt_list[i][k-1][0]
                    row['adj_open'] = NaN 
                    row['adj_close'] = NaN
                    row['adj_high'] = NaN
                    row['adj_low'] = NaN
                    row['close'] = NaN
                    row['volume'] = NaN
                    parseddate = time.strptime(timestamps[j],'%Y%m%d')
                    row['timestamp'] = timestamps[j]
                    row['when_available'] = time.mktime(parseddate)
                    row['interval'] = 86400
                    self.priceArray[j,i] = row
                    
                
            
        
    

