#program that takes in brightness time series and Bayesian changepoint information 
#outputs brightness between change points
#useful for generating the histogram of brightness between well-separated changepoints

import csv
import numpy
import itertools as it
import sys

filenumber=sys.argv[1] #command line argument



bcpfile = open("changepoints/"+filenumber+".bcp") #Bayesian change point probabilities file
brightnessfile = open(filenumber+".brightness.q") #brightness file
bcpcsv=csv.reader(bcpfile)
brightnesscsv=csv.reader(brightnessfile)

bcp=[]
brightness=[]


#skip last value of Bayesian probabilities as it's a NA
for row in bcpcsv:
    if('NA'!= row[0]): #skip the last row
        bcp.append(float(row[0])) #convert string in first and only column to float

for row in brightnesscsv:
    brightness.append(float(row[0])) #convert string in first and only column to float


ischangepoint=([i>.5 for i in bcp]) #true if probability of changing is > .5

durationwithoutchanges=[]


#we are looking for stretches without a changepoint and labeling them with the length of the stretch

for i in range(len(ischangepoint)):
    if(False==ischangepoint[i]): #if it's not a changepoint, label it with zero duration
            durationwithoutchanges.append(0)
    else:#if it is a changepoint
        j=i+1

        #skip all the elements that are not changepoints
        while (j<len(ischangepoint) and False==ischangepoint[j] ):
            j=j+1

        if(j<(len(ischangepoint)-1)):
            durationwithoutchanges.append(j-i)

        #don't bother dealing with handling the end of the data

#sort change points decending and return index
#first value will be index of longest brightness level
sortedindices = sorted(range(len(ischangepoint)),reverse=True,key = lambda i: ischangepoint[i])

#top three brightness ranges without change points
first=brightness[sortedindices[1]:(sortedindices[1]+durationwithoutchanges[sortedindices[1]])]
second=brightness[sortedindices[2]:(sortedindices[2]+durationwithoutchanges[sortedindices[2]])]
third=brightness[sortedindices[3]:(sortedindices[3]+durationwithoutchanges[sortedindices[3]])]

#brightness data without the top three ranges lacking changepoints
remainder=(brightness[0:sortedindices[1]] #beginning to first range
    +brightness[sortedindices[1]+durationwithoutchanges[sortedindices[1]]:sortedindices[2]] #end of first range to second range
    +brightness[sortedindices[2]+durationwithoutchanges[sortedindices[2]]:sortedindices[3]] #end of second range to third range
    +brightness[sortedindices[3]+durationwithoutchanges[sortedindices[3]]:]) #end of third range to fourth range
    
with open("split/"+filenumber+"split.csv", 'w') as f:
    csv.writer(f,delimiter='\t').writerows(it.zip_longest(remainder,first, second,third))

bcpfile.close()
brightnessfile.close()
f.close()
