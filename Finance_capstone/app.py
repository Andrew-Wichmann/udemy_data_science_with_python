"""
From Jose Portilla's Udemy course (https://www.udemy.com/python-for-data-science-and-machine-learning-bootcamp/learn/v4/overview)
Read in market data and display graphes to explore the 2008 financial crash
"""
#BEGIN IMPORTS
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
cf.go_offline()

#END IMPORTS
#BEGIN DATA CLEANING/PREP

#Create start and end datetime objects
start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2017, 5, 20)

#Create bank dataframes by pulling from Google Finance
BAC = data.DataReader("BAC", 'google', start, end)
C = data.DataReader("C", 'google', start, end)
GS = data.DataReader("GS", 'google', start, end)
JPM = data.DataReader("JPM", 'google', start, end)
MS = data.DataReader("MS", 'google', start, end)
WFC = data.DataReader("WFC", 'google', start, end)

#Create ticker labels
tickers='BAC C GS JPM MS WFC'.split()
tickers.sort()

#Concatenate all dataframes into one big dataframe
bank_stocks=pd.concat([BAC, C, GS, JPM, MS, WFC], keys=tickers, axis=1)

#Rename columns
bank_stocks.columns.names = ['Bank Ticker','Stock Info']

#Create dataframe with returns
returns = pd.DataFrame()
for tick in tickers:
    returns[tick] = bank_stocks[tick]['Close'].pct_change()


#END DATA CLEANING/PREP
#BEGIN PLOTING

#Plot and show graph of the comparative returns for each bank
sns.pairplot(returns[1:])
plt.show()

#Plot Morgan Stanley returns for the year 2015
sns.distplot(returns.ix['2015-01-01' : '2015-12-31']['MS'],color='green',bins=100)
plt.show()

#Plot CitiBank returns for the year 2015
sns.distplot(returns.ix['2015-01-01' : '2015-12-31']['C'],color='red',bins=100)
plt.show()

bank_stocks.xs('Close', axis=1, level=1).iplot()
plt.show()

#Make a heatmap of the correlations between bank returns
sns.heatmap(bank_stocks.xs('Close', axis=1, level=1).corr(), annot=True)
plt.show()

bank_stocks['BAC', 'Close'].rolling(window=30).mean()[29:]
plt.show()

#Make a clustermap of the correlations between bank returns
sns.clustermap(bank_stocks.xs('Close', axis=1, level=1).corr(), annot=True)
plt.show()

bank_stocks['BAC'][['Open', 'High', 'Low', 'Close']].ix['2015-01-01':'2016-01-01'].iplot(kind='candle')

bank_stocks['MS']['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='sma', periods=[14,15,100])
plt.show()

bank_stocks['BAC'].loc['2015-01-01':'2016-01-01'].ta_plot(study='boll')
plt.show()