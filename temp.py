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
F = 0.005   # 0.5% Brokerage fee
csvdata = pd.read_csv("DATA.csv")
 
#%%
def GetData(NameOfFile):
  csvdata = pd.read_csv(NameOfFile)
  return csvdata  # pd.DataFrame Object
#%%
def PartitionData(Data):
 Endindex=[]
 Listofdates=[]
 DateToIndex = {}
 for i in range (0,len(Data.ind)):

  if Data.datadate[i] in DateToIndex.keys():
    DateToIndex[Data.datadate[i]].append(i)
  else:
    DateToIndex[Data.datadate[i]] = [i]
    Endindex.append(i)
 Endindex.append(len(Data.ind))
 for xyz in range (0,len(Endindex)-1):
     Listofdates.append(Data.iloc[int(Endindex[xyz]):int(Endindex[xyz+1])])




    






 return Listofdates,DateToIndex    # List containing of the Data Partitioned according to Date, and the Dictionary mapping Dates to their index in the list 
#%%
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
  meanprice = (todayprice+Ndaybackprice)/2
  print(meanprice)
  momentumbymean = momentum/meanprice
  return momentumbymean
#%% 
def GetBalanced(prices, weights,balance):
  # prices : Numpy array containing Prices of all the 30 Stocks
  # weights : Multi-hot Numpy Array : The Elements corresponding to stocks which are to be bought(Top M Stocks with positive Momentum Indicator) are set to their priority, All other elements are set to zero.
   # Returns Numpy array containing the number of shares to buy for each stock!
  a = sorted(weights)
  i=4
  for j in range(5,30):
      a[j]=0
  while i>=1:
      if a[i]>0:
          break
      # elif j==0:
      #     print("There are no prmising stocks. Consider not investing.")
      else:
          a[i]=0
          i=i-1
  for k in range(0,30):
      if weights[k]<a[i]:
          weights[k]=0 
  vector = np.vectorize(float)
  weights = vector(weights)  
  weightedweight=weights/sum(weights)
  moneyineachstock=float(balance)*weightedweight
  numberofstocks=moneyineachstock/(vector(prices)*(1+F))
  return numberofstocks     
#%%
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
#%%
myPortfolio = PortFolio(99999,99999,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
NetWorthAfterEachTrade = [99999]


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
  # Check if you need to rebalance Portfolio's Today
  if (i%T)==0 :
        myPortfolio.RebalancePortFolio(GetMomentumBasedPriority(PartitionedData, DateToIndex ,today))
  print(i)
  # If so, do it by Calling first the GetMomentumBasedPriority function and then passing it to the rebalance function
print("Thanks for viewing")
print(NetWorthAfterEachTrade)
#%%
def VizualizeData(NetWorthAfterEachTrade):
 

      

































 