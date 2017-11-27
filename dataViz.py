# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:03:18 2017

@author: cwaldoch
"""
import numpy as np
import pandas as pd
import os, pdb, datetime, sys
import matplotlib.pyplot as plt
import matplotlib

tripData = pd.read_csv(r'results.csv')

tripData['datetime'] = pd.to_datetime(tripData['Time'].values)
sortedData = tripData.sort_values('datetime', ascending = True)
sortedData = sortedData.reset_index(drop = True)
# timeDelta.item()/1e9/60 to get it in minutes
# need to drop sale rows to just transfer eit and entry

results = []
i = 0
for idx in range(0, len(sortedData)-3):
    #pdb.set_trace()
    row = sortedData.loc[idx]
    rowMiddle = sortedData.loc[idx+1]
    rowVerify = sortedData.loc[idx+2]
    
    if row['Description'] == 'Entry' and rowVerify['Description'] == 'Transfer' and rowMiddle['Description'] == 'Exit':
        try:
            rowMiddle = sortedData.loc[idx+1]
            print(str(row['datetime']) + ' ' + row['Entry Location/ Bus Route'])
            print(str(rowMiddle['datetime']) + ' ' + rowMiddle['Exit Location'])
            print(str(rowVerify['datetime']) + ' ' + rowVerify['Entry Location/ Bus Route'])
            #pdb.set_trace()
            results.append([(rowVerify['datetime']-row['datetime']),
                            'trip_'+str(i), 'To Work', row['datetime'],
                            rowVerify['datetime']+pd.Timedelta(minutes=10)])
            i = i + 1
            
        except TypeError:
            pdb.set_trace()
            
    if row['Description'] == 'Entry' and rowVerify['Description'] == 'Exit' and rowMiddle['Description'] == 'Transfer':
        try:
            rowMiddle = sortedData.loc[idx+1]
            print(str(row['datetime']) + ' ' + row['Entry Location/ Bus Route'])
            print(str(rowMiddle['datetime']) + ' ' + rowMiddle['Exit Location'])
            print(str(rowVerify['datetime']) + ' ' + rowVerify['Exit Location'])
            
            results.append([(rowVerify['datetime']-row['datetime']),
                            'trip_'+str(i), 'From Work', row['datetime'],
                            rowVerify['datetime']+pd.Timedelta(minutes=10)])
            i = i + 1
            
        except TypeError:
            pdb.set_trace()
            
dfCommute = pd.DataFrame(results, columns = ['time', 'Trip Number', 'Trip Type', 'Start Datetime', 'Stop Datetime'])
commuteSorted = dfCommute.sort_values('time', ascending = True)

commuteMinutes = [x.item()/1e9/60 for x in commuteSorted['time'].values]
commuteSorted['minutes'] = commuteMinutes

commuteSorted['startMinutes'] = commuteSorted['Start Datetime'].dt.round('min')
commuteSorted['stopMinutes'] = commuteSorted['Stop Datetime'].dt.round('min')



startTimes = commuteSorted['startMinutes'].dt.time
stopTimes = commuteSorted['stopMinutes'].dt.time

commuteSorted['Start Time'] = startTimes
commuteSorted['Stop Time'] = stopTimes


commuteSorted.to_csv('testingcmtedata.csv')

commuteTimes = commuteSorted['minutes'].values

toWork = commuteSorted[commuteSorted['Trip Type'] == 'To Work']
fromWork = commuteSorted[commuteSorted['Trip Type'] == 'From Work']

commuteSorted = commuteSorted[commuteSorted['Trip Type'] == 'To Work']
uTrips = list(set(commuteSorted['Trip Number'].values))

graphingDict = {}

listTimings = []

for uTrip in uTrips:
    dfTrip = commuteSorted[commuteSorted['Trip Number'] == uTrip]
    timing = pd.Series(pd.date_range(dfTrip['startMinutes'].values[0],
                                     dfTrip['stopMinutes'].values[0],
                                     freq='1min')).dt.time
    #timingTimes = pd.to_datetime(timing).time
    listTimings.append(timing)

    
allTimings = []

for x in listTimings:
    for y in x:
        allTimings.append(y)

uTimings = list(set(allTimings))

graphResults = []

df1 = pd.DataFrame(allTimings, columns=['Times'])
for timing in uTimings:
    dfTime = df1[df1['Times'] == timing]
    timingCount = len(dfTime)
    graphResults.append([timing, timingCount])
    
dfGraph = pd.DataFrame(graphResults, columns = ['time', 'count'])
sortedGraph = dfGraph.sort_values('time', ascending = True)
    

ind = np.arange(0, len(sortedGraph))
plt.bar(ind, sortedGraph['count'])

plt.xticks(ind+1.5, sortedGraph['time'].values, rotation=90)
matplotlib.rcParams.update({'font.size': 10})

plt.ylabel('Minute Trip Overlap Count')
plt.xlabel('Time')



"""
get max end and min start times for each trip set (from/to work)
create a minute range for each trip that covers all of the relevant minutes
graph minutes based on a y axis of count and an x axis of minutes

"""

#for commute in commuteTimes:
#    commuteRange = list(range(0, int(np.round(commute))))
#    plt.plot(commuteRange)
#    
#plt.show()
#    



















