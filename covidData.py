import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#   list of states we are sampling
#   just using a few for testing
#   todo should create this list by pulling info from party file
stateList = ['Alabama', 'Arizona', 'Arkansas', 'Colorado', "Delaware"]

#   NYT data repositories

#   USA as a whole
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
#   state level data
urlState = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'


#   turn data sets into dataframes
data = pd.read_csv(url)
dataState = pd.read_csv(urlState, parse_dates=['date'])
#   read in data set containing party data for each state
partyData = pd.read_csv('party.csv')


#   make new data set combining state and party data
mix = pd.merge(dataState, partyData, on="state")
#   print the tail to check merging was done correctly
print(mix.tail())


#   index data set based on date
mix['date'] = pd.to_datetime(mix['date'])
#   create different dataframes for states with republican and democratic governors
mixDemocrat = mix
mixDemocrat = mixDemocrat[mixDemocrat.Governor == 'D']
mixRepublican = mix
mixRepublican = mixRepublican[mixRepublican.Governor == "R"]


#   turn mix into dataframes
dataframe = pd.DataFrame(mix)
dataframer = pd.DataFrame(mixRepublican)
dataframed = pd.DataFrame(mixDemocrat)


#   function that plots all states in states list data
#   todo function can only take 'deaths' or 'cases' as argument, need to add error handling
def stateData(y):
    #   set y axis label
    plt.ylabel(y)

    #   loop through state list and plot each state on the same graph
    for x in range(len(stateList)):
        #   variable we use to
        ax = plt.gca()
        #   select only current state
        dataframe2 = dataframe.loc[dataframe['state'] == stateList[x]]
        # plot current state
        dataframe2.plot(x='date', label=stateList[x], y=y, ax=ax)
    plt.show()

#   function that displays state level data on a per capita basis
def stateDataCapita(y):
    #   set y axis label
    plt.ylabel(y+' per 100,000')

    #   loop through state list and plot each state on the same graph
    for x in range(len(stateList)):
        #   variable we use to
        ax = plt.gca()
        #   select only current state
        dataframe2 = dataframe.loc[dataframe['state'] == stateList[x]]
        # plot current state
        dataframe2.plot(x='date', label=stateList[x], y=('per_100000_'+y), ax=ax)
    plt.show()
    
#   function that sums states by governor party and plots
def stateparty(y):
    #   set y axis label
    plt.ylabel(y)
    #   create base plot
    ax = plt.gca()
    #   plot republican states
    dataframe3 = dataframer.resample('D', on='date')[y].sum()
    dataframe3.plot(x='date', label='Republican Governor', y=y, ax=ax)
    #   plot democrat states
    dataframe4 = mixDemocrat.resample('D', on='date')[y].sum()
    dataframe4.plot(x='date', label='Democrat Governor', y=y,  ax=ax)
    #   add labels
    plt.legend()
    #   plot
    plt.show()


#   run statedata function
stateData('cases')
stateData('deaths')
stateparty('cases')
stateparty('deaths')
