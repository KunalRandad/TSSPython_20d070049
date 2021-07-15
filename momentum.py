{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "U1k32GLIm1o5"
   },
   "source": [
    "## Momentum \n",
    "\n",
    "Momentum-based Trading is based on the assumption that Stocks which have performed will in the past, will perform better in the coming future.\n",
    " \n",
    "To define 'past', we take a variable **N**, and say that : \n",
    "\n",
    "<centre> Momentum(For A particular stock) = Close Price(Today) - Close Price(N-day ago) </centre>\n",
    "\n",
    "This gives us our first hyper-parameter (parameters of the model which could be changed in order to improve the model) : **N**\n",
    "\n",
    "We would also be reshuffling our [Portfolio](https://www.investopedia.com/terms/p/portfolio.asp) at certain intervals of time, which gives us our second hyper-parameter: **T** (The time after which we'll be reshuffling our Portfolio)\n",
    "\n",
    "Its never suggested to keep all your money invested, you must have some risk-free assets as well, so that even if you lose some of your cash in trading, you could still place better bets and regain that lost cash, Thus, We get our third Hyper-parameter: **R**, The Ratio of Total Balance, which we will using for investing.\n",
    "\n",
    "You will not be investing in all the 30 Tickers now, Will you? You will choose the top few stocks, which show the highest promise in terms of Momentum, which brings us to another hyper-parameter: **M**, The Number of Top few stocks (based on Momentum), which you'll keep in your Portfolio.\n",
    "\n",
    "Finally, There's some brokerage fee which you need to pay in order to place orders on the stock market, typically its less than 0.05% of the total amount : **F**\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {
    "id": "GpkE6S0ZjSlB"
   },
   "outputs": [],
   "source": [
    "#Importing Required Libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import datetime\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "#Declaring the Hyperparameters\n",
    "\n",
    "N = 50\n",
    "T = 7\n",
    "R = 0.8\n",
    "M = 5\n",
    "F = 0.0005   # 0.5% Brokerage fee"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "DwPazs3-q618"
   },
   "source": [
    "The Second step would be to define a function which reads the Prices of various Stocks into memory.\n",
    "\n",
    "In the file DATA.csv , which we had uploaded in our repository, we have prices of 30 firms enlisted in S & P 500 Index (Apple, IBM, Cisco, Walmart and the like!) from 2nd January 2009 to 17th August 2020.\n",
    "\n",
    "For our purposes, We'll only be requiring certain columns. On an honest note, Just getting the Columns on Ticker, Date and Adjusted Closing Price would do the job, but if you want, you may take Opening Price as well.\n",
    "\n",
    "Read up about the [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) function from here, and figure out how you'll use it to do the job (You don't need all the columns!) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {
    "id": "9rsbAPafuUk1"
   },
   "outputs": [],
   "source": [
    "def GetData(NameOfFile):\n",
    "  csvdata = pd.read_csv(NameOfFile)\n",
    "  return csvdata  # pd.DataFrame Object"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "qkWJ29Kquf2B"
   },
   "source": [
    "To aid Data-Manipulation, it would be beneficial, if we split the DataFrame into many small parts each corresponding to the data corresponding to the 30 Tickers on a particular date. These small parts could then be stored in a list.\n",
    "\n",
    "We would also be needing to remember which date is at what index, so that we can use that later. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {
    "id": "d4HLxmu9HTl8"
   },
   "outputs": [],
   "source": [
    "def PartitionData(Data):\n",
    " Endindex=[]\n",
    " Listofdates=[]\n",
    " DateToIndex = {}\n",
    " for q in range (0,len(Data.ind)):\n",
    "\n",
    "  if Data.datadate[q] in DateToIndex.keys():\n",
    "    DateToIndex[Data.datadate[q]].append(q)\n",
    "  else:\n",
    "    DateToIndex[Data.datadate[q]] = [q]\n",
    "    Endindex.append(q)\n",
    " Endindex.append(len(Data.ind))\n",
    " for xyz in range (0,len(Endindex)-1):\n",
    "     Listofdates.append(Data.iloc[int(Endindex[xyz]):int(Endindex[xyz+1])])\n",
    " return Listofdates,DateToIndex    # List containing of the Data Partitioned according to Date, and the Dictionary mapping Dates to their index in the list "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "peRRNuUQOnVM"
   },
   "source": [
    "Now, We need a function to calculate the Momentum value for all of our 30 Tickers.\n",
    "To do this, We need to have a few things in mind:\n",
    "\n",
    "\n",
    "1.   We need to start at Nth day in our list, as only then we'll be able to calculate the Momentum (This will be taken care of by later parts of the Program, when we actually run the Model)\n",
    "\n",
    "2.   The Stock Market isn't open on all days, so we often won't be able to go N days behind, and will have to take the closest value instead(We can't just go N entries behind in the List we created and expect that to work, Why?) In order to work with dates, you should get to know more about the datetime library of Python from [here](https://thispointer.com/python-how-to-convert-datetime-object-to-string-using-datetime-strftime/) (Especially the datetime.strftime() function) and about the [datetime.timedelta()](https://www.studytonight.com/python-howtos/how-to-add-days-to-date-in-python) function.\n",
    "\n",
    "Also, as you may have figured it out yourself, while DataFrames are great for Data Handling and small statistical calculations, They aren't so for big calculations as the Numpy Library has both a richer variety of functions for such manipulations and is also more efficient!\n",
    "\n",
    "After we calculate the Momentum for all our Tickers, it would be a great thing to do, if we could divide their prices by their mean(in the N day interval, as we need to see which stock outperforms others and in order to do this, it won't be fair if we take the absolute growth in numbers!(Why?)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {
    "id": "tMKHAcBnSG5n"
   },
   "outputs": [],
   "source": [
    "def GetMomentumBasedPriority(PartitionedDataFrameList, DateToIndex ,today):\n",
    "  # PartitionedDataFrameList : Pandas DataFrame, The Output of your last function\n",
    "  # DateToIndex : Dictionary mapping dates to their index in the PartitionedDataFrameList\n",
    "  # today :  Today's date (string) In Format: YYYYMMDD\n",
    "\n",
    "\n",
    "  #NdaysAgo is a datatime.date() object contining the required data, you need to convert it to a string and then check if its\n",
    "  #actually there in the Data you have or will you have to get going using some other nearest date\n",
    "  today=str(today)\n",
    "  NdaysAgo = datetime.date(int(today[0:4]),int(today[4:6]),int(today[6:])) + datetime.timedelta(days = -N)\n",
    "  a=NdaysAgo.strftime('%Y%m%d')\n",
    "  arr = np.array(PartitionedDataFrameList)\n",
    "  vector = np.vectorize(float)\n",
    "  while True:\n",
    "       if int(a) in DateToIndex.keys() :\n",
    "                      break\n",
    "       else:\n",
    "         a=str(a)\n",
    "         NdaysAgo = datetime.date(int(a[0:4]),int(a[4:6]),int(a[6:8])) + datetime.timedelta(days = -1)\n",
    "         a=NdaysAgo.strftime('%Y%m%d')\n",
    "        \n",
    "  todayprice=[]\n",
    "  Ndaybackprice=[]\n",
    "  for i in range (0,30):\n",
    "      todayprice.append(arr[int((DateToIndex[int(today)][0])/30)][i][3])\n",
    "      Ndaybackprice.append(arr[int((DateToIndex[int(a)][0])/30)][i][3])\n",
    "  todayprice = vector(todayprice)\n",
    "  Ndaybackprice = vector(Ndaybackprice)\n",
    "  momentum=todayprice-Ndaybackprice\n",
    "  meanprice = (todayprice+Ndaybackprice)/2 #INSTEAD OF TAKING AVERAGE OVER LAST N DAYS, I HAVE TAKEN AVERAGE OVER LAST N'th DAY AND TODAY \n",
    "  momentumbymean = momentum/meanprice\n",
    "  return momentumbymean"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "s5QOHJ9Ra00l"
   },
   "source": [
    "Even after you have got your Momentum-based priorities, and have decided which stocks to buy and what will be the weight of each, you still need to figure out how much of each will you buy. To do this, first you'll sell all your pre-owned stocks which will increase your cash in hand, then you'll know the stocks to buy and their relative weights (given by their Momentum/mean) and you need a function which tells you how many stocks to buy for each ticker!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {
    "id": "cQg8OWVg_qo5"
   },
   "outputs": [],
   "source": [
    "def GetBalanced(prices, weights,balance):\n",
    "  # prices : Numpy array containing Prices of all the 30 Stocks\n",
    "  # weights : Multi-hot Numpy Array : The Elements corresponding to stocks which are to be bought(Top M Stocks with positive Momentum Indicator) are set to their priority, All other elements are set to zero.\n",
    "   # Returns Numpy array containing the number of shares to buy for each stock!\n",
    "  a = sorted(weights)\n",
    "  y=4\n",
    "  for j in range(5,30):\n",
    "      a[j]=0\n",
    "  while y>=1:\n",
    "      if a[y]>0:\n",
    "          break\n",
    "      # elif j==0:\n",
    "      #     print(\"There are no prmising stocks. Consider not investing.\")\n",
    "      else:\n",
    "          a[y]=0\n",
    "          y=y-1\n",
    "  for h in range(0,30):\n",
    "      if weights[h]<a[h]:\n",
    "          weights[h]=0 \n",
    "  vector = np.vectorize(float)\n",
    "  weights = vector(weights)  \n",
    "  weightedweight=weights/sum(weights)\n",
    "  moneyineachstock=float(balance)*weightedweight\n",
    "  numberofstocks=moneyineachstock/(vector(prices)*(1+F))\n",
    "  return numberofstocks "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "WWN9ri-rIb3e"
   },
   "source": [
    "Now, We need something to simulate our [Portfolio](https://www.investopedia.com/terms/p/portfolio.asp). In order to do that we need a class, which has certain  basic features and functionalities.\n",
    "\n",
    "Features : \n",
    "\n",
    "\n",
    "1.   Your Initial Balance\n",
    "2.   Your Current Balance\n",
    "3.   A list(/any other container) storing the number of stocks of each ticker currently in possession. (Numpy Array prefered)\n",
    "4.   Most recent prices of all the stocks (As a Numpy array)\n",
    "\n",
    "Functionalities: \n",
    "\n",
    "\n",
    "\n",
    "1.   Calculating current Net Worth (Balance+Total Evaluation of all Stocks owned!) \n",
    "2.   Buying a Particular Stock (Keep the Transaction fee in mind!)\n",
    "3.   Selling a particular Stock whole (Keep the Transaction Fee in mind!)\n",
    "4.   Rebalance Portfolio  (Takes Numpy array as input)\n",
    "5.   Function to change the value of most recent prices stored (Takes Numpy array as input)\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {
    "id": "gi60d9qUNO0_"
   },
   "outputs": [],
   "source": [
    "class PortFolio:\n",
    "  vector = np.vectorize(float)\n",
    "  def __init__(self,initialbalance,currentbalance,stocksiown,prices):\n",
    "   self.initialbalance = initialbalance\n",
    "   self.currentbalance = currentbalance\n",
    "   self.stocksiown = stocksiown\n",
    "   self.prices = prices\n",
    "  \n",
    "  def SellStock(self,index):\n",
    "   self.currentbalance = self.currentbalance+(self.stocksiown[index])*(self.prices[index])*(1-F)\n",
    "   self.stocksiown[index]=0\n",
    "  \n",
    "  def BuyStock(self,index, number):\n",
    "   #index : The index of the Stock to buy (0-29) \n",
    "   #number : Number of shares to buy (float)\n",
    "   self.stocksiown[index] = self.stocksiown[index] + number\n",
    "   self.currentbalance = self.currentbalance - number*(self.prices[index])*(1+F)\n",
    "\n",
    "  def CalculateNetWorth(self):\n",
    "   vector = np.vectorize(float)\n",
    "   #Return Net Worth (All Shares' costs+ Balance)\n",
    "   self.Networth = vector(self.currentbalance) + sum(vector(self.prices)*vector(self.stocksiown))\n",
    "   return self.Networth\n",
    "\n",
    "  def ChangePricesTo(self,newPriceVector):\n",
    "  # newPriceVector : Numpy array containing the prices of all the stocks for the current day\n",
    "   self.prices = newPriceVector\n",
    "\n",
    "  def RebalancePortFolio(self,newWeights):  \n",
    "    # newWeights : Numpy array containing Momentum/Mean for all stocks in the N-day period\n",
    "    # First sell all your pre-owned Stock (make sure to take transaction fee into account!)\n",
    "    for m in range (0,30):\n",
    "        self.SellStock(m)\n",
    "    # This would change your total balance\n",
    "    # Then take the top M(/might be less than M, if >(30-M) had negative Momentum) and send them to the GetBalanced() Function\n",
    "    self.stockstobuy = GetBalanced(self.prices,newWeights,self.currentbalance*R)\n",
    "    # Then take that output and pass them to the BuyStocks function!\n",
    "    for n in range (0,30):\n",
    "        self.BuyStock(n,self.stockstobuy[n])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "PKiLs-6TB6mU"
   },
   "source": [
    "With that the difficult part is over!\n",
    "\n",
    "Now, all you need to work on is a main loop, which calls all these functions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "zjo2KrcaCmqf"
   },
   "outputs": [],
   "source": [
    "myPortfolio = PortFolio(99999,99999,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])\n",
    "NetWorthAfterEachTrade = [99999]\n",
    "day = [N]\n",
    "\n",
    "#First Get the Data\n",
    "Data = GetData(\"DATA.csv\")\n",
    "(PartitionedData, DateToIndex) = PartitionData(Data)\n",
    "\n",
    "\n",
    "\n",
    "#Start processing from the (N+1)th Day(among the ones recorded in the Data)\n",
    "for i in range(N+1,int((len(Data.ind))/30)):\n",
    "  today=Data.datadate[30*i]\n",
    "  # Change the Prices to the ith Term\n",
    "  for k in range (0,30):\n",
    "        bruh=PartitionedData[i]\n",
    "        bruhh = bruh.iloc[k]\n",
    "        myPortfolio.prices[k] = bruhh[3]\n",
    "  # Get NetWorth and store in list\n",
    "  NetWorthAfterEachTrade.append(myPortfolio.CalculateNetWorth())\n",
    "  day.append(i)\n",
    "  # Check if you need to rebalance Portfolio's Today\n",
    "  if (i%T)==0 :\n",
    "        myPortfolio.RebalancePortFolio(GetMomentumBasedPriority(PartitionedData, DateToIndex ,today))\n",
    "    # If so, do it by Calling first the GetMomentumBasedPriority function and then passing it to the rebalance function\n",
    "print(\"Thanks for viewing\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "rHB126bDE2Kn"
   },
   "source": [
    "##Moment of Truth\n",
    "\n",
    "Time to check, if your Program actually works!\n",
    "\n",
    "Plot the data you collected in various ways and see if what you did worked!\n",
    "\n",
    "Feel free to use whichever one of Matplotlib or Seaborn you want to.\n",
    "\n",
    "You should try changing the hyper-parameters to increase(/decrease) your performance!\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "Z3AVQq09FxYm"
   },
   "outputs": [],
   "source": [
    "def VizualizeData():\n",
    "    plt.plot(day,NetWorthAfterEachTrade)\n",
    "    plt.ylabel('Total Net Worth')\n",
    "    plt.xlabel('Number of working days')\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "cZoWhY8X9BSR"
   },
   "source": [
    "You may use this cell to write about what results you got!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "colab": {
   "collapsed_sections": [],
   "name": "Momentum.ipynb",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
