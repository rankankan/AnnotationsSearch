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

import os, sys

# Used only for testing
infile = "text_annotations_flywire.txt"
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

#####                   #######
##### Main Program      #######
#####                   #######
    
try:
   sys.argv[1]
except IndexError:
   print ("Error - missing string to search - Usage ./findann.py string")
   sys.exit(1)
else:
   searchString = sys.argv[1].lower()

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

#applying loop
cnt = 0
for i in range(len(filenameList)):
    if (searchString in filenameList[i]):
        resultsList.append(i)   
print("\nThe string " +  searchString + " was found " + str(len(resultsList)) + " times under the following indices: \n")
print(resultsList)

