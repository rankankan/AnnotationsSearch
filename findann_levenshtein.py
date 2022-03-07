# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 13:47:53 2022

@author: rankankan
"""

#!/usr/bin/python

# It searches for all entries that contain the substring provided as a parameter.
# It returns a list of all indices that contain that substring
# The code makes use of the memcached mechanism in order to trigger data refresh at 
# configurable intervals. The code will be optimized once the format of the data that the 
# cache stores is decided. 

import os, sys, re, numpy, time

# Used only for testing - Candidates for parametrization 
infile = "text_annotations_flywire.txt"
levenshteinThreshold = 2

filenameList = []

from pymemcache.client import base

# Wrapper for call to get current annotation data.
# Call signature, format of data and data structure of result to be defined.
def refresh_cache():
# Placeholder function
    read_file_into_memory()
    return(filenameList)

def read_file_into_memory():
    # Check on whether file exists and is accessible
    if not os.path.isfile(infile):
       print ("Error - input file", infile, "not available") 
       sys.exit(1)
    else:
        f = open(infile, "r")
 
# Normally, only the updates will be appended to the list when a cache refresh is required.
    for line in f:
         line = preprocess(line)
         filenameList.append(line)
    f.close()
    print("\nNumber of lines read into memory: " + str(len(filenameList)))
    
# Placeholder for possible future tokenization, etc.
def preprocess(line):
    line = line.lower();
    return (line)

def measureLevenshteinDistance(searchedWord, annotationWord):
    distanceMatrix = numpy.zeros((len(searchedWord) + 1, len(annotationWord) + 1))

    for searchedIndex in range(len(searchedWord) + 1):
        distanceMatrix[searchedIndex][0] = searchedIndex

    for annotatedIndex in range(len(annotationWord) + 1):
        distanceMatrix[0][annotatedIndex] = annotatedIndex
        
    char1 = 0
    char2 = 0
    char3 = 0
    
    for searchedIndex in range(1, len(searchedWord) + 1):
        for annotatedIndex in range(1, len(annotationWord) + 1):
            if (searchedWord[searchedIndex-1] == annotationWord[annotatedIndex-1]):
                distanceMatrix[searchedIndex][annotatedIndex] = distanceMatrix[searchedIndex - 1][annotatedIndex - 1]
            else:
                char1 = distanceMatrix[searchedIndex][annotatedIndex - 1]
                char2 = distanceMatrix[searchedIndex - 1][annotatedIndex]
                char3 = distanceMatrix[searchedIndex - 1][annotatedIndex - 1]
                
                if (char1 <= char2 and char1 <= char3):
                    distanceMatrix[searchedIndex][annotatedIndex] = char1 + 1
                elif (char2 <= char1 and char2 <= char3):
                    distanceMatrix[searchedIndex][annotatedIndex] = char2 + 1
                else:
                    distanceMatrix[searchedIndex][annotatedIndex] = char3 + 1
    return distanceMatrix[len(searchedWord)][len(annotationWord)]

def printdistanceMatrix(distanceMatrix, searchedWordLength, annotationWordLength):
    for searchedIndex in range(searchedWordLength + 1):
        for annotatedIndex in range(annotationWordLength + 1):
            print(int(distanceMatrix[searchedIndex][annotatedIndex]), end=" ")
        


#####                   #######
##### Main Program      #######
#####                   #######
    
#try:
#   sys.argv[1]
#except IndexError:
#   print ("Error - missing string to search - Usage ./findann.py string")
#   sys.exit(1)
#else:
#   searchString = sys.argv[1].lower()
searchString = "putative"

# Initialization to get memcached working
# It will  need to be set properly to work with server
# *Note*: memcached must have been started *prior* to running this code.
    
client = base.Client(('localhost', 11211))
result = client.get('annotations')

if (isinstance(result, type(None))):
    # The cache is empty, need to get the data a very first time
    result = refresh_cache()
    # Cache the data for subsequent accesses:
    client.set('annotations', result)


#List of matched indices 
resultsList = []
similarList = []
totalDistance = 0

#applying loop
start_time = time.process_time()
cnt = 0
for i in range(len(filenameList)):
    words = re.split('[;,.\s]+', filenameList[i])
    for j in range(len(words)):
        totalDistance = measureLevenshteinDistance(searchString, words[j])
        if (totalDistance <= levenshteinThreshold):
            if(totalDistance == 0):
                resultsList.append(i)
            else:
                similarList.append(i)
            break
                
print("\nThe string " +  searchString + " was found " + str(len(resultsList)) + " times under the following indices: \n")
print(resultsList)
print("\nClose matches were found " + str(len(similarList)) + " times under the following indices: \n")
print(similarList)
end_time = time.process_time()
print("\nElapsed time: ",end_time - start_time)

