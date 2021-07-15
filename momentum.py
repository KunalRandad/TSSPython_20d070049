## Momentum 

Momentum-based Trading is based on the assumption that Stocks which have performed will in the past, will perform better in the coming future.
 
To define 'past', we take a variable **N**, and say that : 

<centre> Momentum(For A particular stock) = Close Price(Today) - Close Price(N-day ago) </centre>

This gives us our first hyper-parameter (parameters of the model which could be changed in order to improve the model) : **N**

We would also be reshuffling our [Portfolio](https://www.investopedia.com/terms/p/portfolio.asp) at certain intervals of time, which gives us our second hyper-parameter: **T** (The time after which we'll be reshuffling our Portfolio)

Its never suggested to keep all your money invested, you must have some risk-free assets as well, so that even if you lose some of your cash in trading, you could still place better bets and regain that lost cash, Thus, We get our third Hyper-parameter: **R**, The Ratio of Total Balance, which we will using for investing.

You will not be investing in all the 30 Tickers now, Will you? You will choose the top few stocks, which show the highest promise in terms of Momentum, which brings us to another hyper-parameter: **M**, The Number of Top few stocks (based on Momentum), which you'll keep in your Portfolio.

Finally, There's some brokerage fee which you need to pay in order to place orders on the stock market, typically its less than 0.05% of the total amount : **F**


#Importing Required Libraries
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#Declaring the Hyperparameters

N = 50
T = 7
R = 0.8
M = 5
F = 0.0005   # 0.05% Brokerage fee

The Second step would be to define a function which reads the Prices of various Stocks into memory.

In the file DATA.csv , which we had uploaded in our repository, we have prices of 30 firms enlisted in S & P 500 Index (Apple, IBM, Cisco, Walmart and the like!) from 2nd January 2009 to 17th August 2020.

For our purposes, We'll only be requiring certain columns. On an honest note, Just getting the Columns on Ticker, Date and Adjusted Closing Price would do the job, but if you want, you may take Opening Price as well.

Read up about the [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) function from here, and figure out how you'll use it to do the job (You don't need all the columns!) 

def GetData(NameOfFile):
  csvdata = pd.read_csv(NameOfFile)
  return csvdata  # pd.DataFrame Object

To aid Data-Manipulation, it would be beneficial, if we split the DataFrame into many small parts each corresponding to the data corresponding to the 30 Tickers on a particular date. These small parts could then be stored in a list.

We would also be needing to remember which date is at what index, so that we can use that later. 

def PartitionData(Data):
 Endindex=[]
 Listofdates=[]
 DateToIndex = {}
 for q in range (0,len(Data.ind)):

  if Data.datadate[q] in DateToIndex.keys():
    DateToIndex[Data.datadate[q]].append(q)
  else:
    DateToIndex[Data.datadate[q]] = [q]
    Endindex.append(q)
 Endindex.append(len(Data.ind))
 for xyz in range (0,len(Endindex)-1):
     Listofdates.append(Data.iloc[int(Endindex[xyz]):int(Endindex[xyz+1])])
 return Listofdates,DateToIndex    # List containing of the Data Partitioned according to Date, and the Dictionary mapping Dates to their index in the list 

Now, We need a function to calculate the Momentum value for all of our 30 Tickers.
To do this, We need to have a few things in mind:


1.   We need to start at Nth day in our list, as only then we'll be able to calculate the Momentum (This will be taken care of by later parts of the Program, when we actually run the Model)

2.   The Stock Market isn't open on all days, so we often won't be able to go N days behind, and will have to take the closest value instead(We can't just go N entries behind in the List we created and expect that to work, Why?) In order to work with dates, you should get to know more about the datetime library of Python from [here](https://thispointer.com/python-how-to-convert-datetime-object-to-string-using-datetime-strftime/) (Especially the datetime.strftime() function) and about the [datetime.timedelta()](https://www.studytonight.com/python-howtos/how-to-add-days-to-date-in-python) function.

Also, as you may have figured it out yourself, while DataFrames are great for Data Handling and small statistical calculations, They aren't so for big calculations as the Numpy Library has both a richer variety of functions for such manipulations and is also more efficient!

After we calculate the Momentum for all our Tickers, it would be a great thing to do, if we could divide their prices by their mean(in the N day interval, as we need to see which stock outperforms others and in order to do this, it won't be fair if we take the absolute growth in numbers!(Why?)



def GetMomentumBasedPriority(PartitionedDataFrameList, DateToIndex ,today):
  # PartitionedDataFrameList : Pandas DataFrame, The Output of your last function
  # DateToIndex : Dictionary mapping dates to their index in the PartitionedDataFrameList
  # today :  Today's date (string) In Format: YYYYMMDD


  #NdaysAgo is a datatime.date() object contining the required data, you need to convert it to a string and then check if its
  #actually there in the Data you have or will you have to get going using some other nearest date
  today=str(today)
  NdaysAgo = datetime.date(int(today[0:4]),int(today[4:6]),int(today[6:])) + datetime.timedelta(days = -N)
  a=NdaysAgo.strftime('%Y%m%d')
  arr = np.array(PartitionedDataFrameList)
  vector = np.vectorize(float)
  while True:
       if int(a) in DateToIndex.keys() :
                      break
       else:
         a=str(a)
         NdaysAgo = datetime.date(int(a[0:4]),int(a[4:6]),int(a[6:8])) + datetime.timedelta(days = -1)
         a=NdaysAgo.strftime('%Y%m%d')
        
  todayprice=[]
  Ndaybackprice=[]
  for i in range (0,30):
      todayprice.append(arr[int((DateToIndex[int(today)][0])/30)][i][3])
      Ndaybackprice.append(arr[int((DateToIndex[int(a)][0])/30)][i][3])
  todayprice = vector(todayprice)
  Ndaybackprice = vector(Ndaybackprice)
  momentum=todayprice-Ndaybackprice
  meanprice = (todayprice+Ndaybackprice)/2 #INSTEAD OF TAKING AVERAGE OVER LAST N DAYS, I HAVE TAKEN AVERAGE OVER LAST N'th DAY AND TODAY 
  momentumbymean = momentum/meanprice
  return momentumbymean

Even after you have got your Momentum-based priorities, and have decided which stocks to buy and what will be the weight of each, you still need to figure out how much of each will you buy. To do this, first you'll sell all your pre-owned stocks which will increase your cash in hand, then you'll know the stocks to buy and their relative weights (given by their Momentum/mean) and you need a function which tells you how many stocks to buy for each ticker!

def GetBalanced(prices, weights,balance):
  # prices : Numpy array containing Prices of all the 30 Stocks
  # weights : Multi-hot Numpy Array : The Elements corresponding to stocks which are to be bought(Top M Stocks with positive Momentum Indicator) are set to their priority, All other elements are set to zero.
   # Returns Numpy array containing the number of shares to buy for each stock!
  a = sorted(weights)
  y=4
  for j in range(5,30):
      a[j]=0
  while y>=1:
      if a[y]>0:
          break
      # elif j==0:
      #     print("There are no prmising stocks. Consider not investing.")
      else:
          a[y]=0
          y=y-1
  for h in range(0,30):
      if weights[h]<a[h]:
          weights[h]=0 
  vector = np.vectorize(float)
  weights = vector(weights)  
  weightedweight=weights/sum(weights)
  moneyineachstock=float(balance)*weightedweight
  numberofstocks=moneyineachstock/(vector(prices)*(1+F))
  return numberofstocks 

Now, We need something to simulate our [Portfolio](https://www.investopedia.com/terms/p/portfolio.asp). In order to do that we need a class, which has certain  basic features and functionalities.

Features : 


1.   Your Initial Balance
2.   Your Current Balance
3.   A list(/any other container) storing the number of stocks of each ticker currently in possession. (Numpy Array prefered)
4.   Most recent prices of all the stocks (As a Numpy array)

Functionalities: 



1.   Calculating current Net Worth (Balance+Total Evaluation of all Stocks owned!) 
2.   Buying a Particular Stock (Keep the Transaction fee in mind!)
3.   Selling a particular Stock whole (Keep the Transaction Fee in mind!)
4.   Rebalance Portfolio  (Takes Numpy array as input)
5.   Function to change the value of most recent prices stored (Takes Numpy array as input)





class PortFolio:
  vector = np.vectorize(float)
  def __init__(self,initialbalance,currentbalance,stocksiown,prices):
   self.initialbalance = initialbalance
   self.currentbalance = currentbalance
   self.stocksiown = stocksiown
   self.prices = prices
  
  def SellStock(self,index):
   self.currentbalance = self.currentbalance+(self.stocksiown[index])*(self.prices[index])*(1-F)
   self.stocksiown[index]=0
  
  def BuyStock(self,index, number):
   #index : The index of the Stock to buy (0-29) 
   #number : Number of shares to buy (float)
   self.stocksiown[index] = self.stocksiown[index] + number
   self.currentbalance = self.currentbalance - number*(self.prices[index])*(1+F)

  def CalculateNetWorth(self):
   vector = np.vectorize(float)
   #Return Net Worth (All Shares' costs+ Balance)
   self.Networth = vector(self.currentbalance) + sum(vector(self.prices)*vector(self.stocksiown))
   return self.Networth

  def ChangePricesTo(self,newPriceVector):
  # newPriceVector : Numpy array containing the prices of all the stocks for the current day
   self.prices = newPriceVector

  def RebalancePortFolio(self,newWeights):  
    # newWeights : Numpy array containing Momentum/Mean for all stocks in the N-day period
    # First sell all your pre-owned Stock (make sure to take transaction fee into account!)
    for m in range (0,30):
        self.SellStock(m)
    # This would change your total balance
    # Then take the top M(/might be less than M, if >(30-M) had negative Momentum) and send them to the GetBalanced() Function
    self.stockstobuy = GetBalanced(self.prices,newWeights,self.currentbalance*R)
    # Then take that output and pass them to the BuyStocks function!
    for n in range (0,30):
        self.BuyStock(n,self.stockstobuy[n])

With that the difficult part is over!

Now, all you need to work on is a main loop, which calls all these functions

myPortfolio = PortFolio(99999,99999,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
NetWorthAfterEachTrade = [99999]
day = [N]

#First Get the Data
Data = GetData("DATA.csv")
(PartitionedData, DateToIndex) = PartitionData(Data)



#Start processing from the (N+1)th Day(among the ones recorded in the Data)
for i in range(N+1,int((len(Data.ind))/30)):
  today=Data.datadate[30*i]
  # Change the Prices to the ith Term
  for k in range (0,30):
        bruh=PartitionedData[i]
        bruhh = bruh.iloc[k]
        myPortfolio.prices[k] = bruhh[3]
  # Get NetWorth and store in list
  NetWorthAfterEachTrade.append(myPortfolio.CalculateNetWorth())
  day.append(i)
  # Check if you need to rebalance Portfolio's Today
  if (i%T)==0 :
        myPortfolio.RebalancePortFolio(GetMomentumBasedPriority(PartitionedData, DateToIndex ,today))
    # If so, do it by Calling first the GetMomentumBasedPriority function and then passing it to the rebalance function
print("Thanks for viewing")

##Moment of Truth

Time to check, if your Program actually works!

Plot the data you collected in various ways and see if what you did worked!

Feel free to use whichever one of Matplotlib or Seaborn you want to.

You should try changing the hyper-parameters to increase(/decrease) your performance!


def VizualizeData():
    plt.plot(day,NetWorthAfterEachTrade)
    plt.ylabel('Total Net Worth')
    plt.xlabel('Number of working days')
    plt.show()

You may use this cell to write about what results you got!

VizualizeData()


## Execute the cell above this to view graph
## I couldnt think of a way to create multiple graphs with different values for N,F,T,etc. Kindly do so manually to evaluate the code
