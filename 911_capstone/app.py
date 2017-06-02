#!/usr/bin/env python
"""Read 911 hotline information display graphs exploring the reasoning behind calls"""
#BEGIN IMPORTS

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#END IMPORTS
#BEGIN DATA CLEANING

#Read in information
df = pd.read_csv('911.csv')

#Create new reasons collumn i.e. EMS, Fire, Traffic
df['Reasons'] = df['title'].apply(lambda x: x.split(':')[0])

#Create time collumns
df['timeStamp'] = df['timeStamp'].apply(pd.to_datetime)
df['Hour'] = df['timeStamp'].apply(lambda x: x.hour)
df['Month'] = df['timeStamp'].apply(lambda x: x.month)
df['Day of Week'] = df['timeStamp'].apply(lambda x: x.dayofweek)
df['Date'] = df['timeStamp'].apply(lambda x: x.date())

#Map ['Day of Week'] and ['Month'] from numbers to human readable names
DMAP = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(DMAP)

MMAP = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'June',
        7:'July', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
df['Month Names'] = df['Month'].map(MMAP)

#Prepare month line plot to fill in missing data
byMonth = df.groupby('Month')
byMonth = byMonth.count()

#Prepare day line plot
dayCount = df.groupby('Date').count()['lat']

#Prepare the heatmap
heatmap = df.groupby(by=['Day of Week','Hour']).count()['Reasons'].unstack()

#END DATA CLEANING
#BEGIN PLOTTING

#Plot and show the instances as a bar graph
sns.countplot(data=df, x='Reasons', palette='magma')
plt.ylabel('Call Count')
plt.show()

#Plot and show the number of calls per day seperated by reason
sns.countplot(data=df, x='Day of Week', hue='Reasons', palette='cool')
plt.legend(bbox_to_anchor=(1, 1))
plt.ylabel('Call Count')
plt.show()

#Plot and show the number of calls per month seperated by reason
sns.countplot(data=df, x='Month Names', hue='Reasons', palette='summer')
plt.legend(bbox_to_anchor=(1, 1))
plt.ylabel('Call Count')
plt.show()

#Plot and show the number of calls as a line graph to estimate Oct/Nov months
sns.lmplot(data=byMonth.reset_index(), x='Month', y='lat')
plt.ylabel('Call Count')
plt.show()

#Plot and show the number of calls per date
dayCount.plot()
plt.ylabel('Call Count')
plt.show()

#Plot and show the heatmap
sns.heatmap(heatmap)
plt.show()
sns.clustermap(heatmap)
plt.show()

#END PLOTTING
