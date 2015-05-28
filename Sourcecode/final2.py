# -*- coding: utf-8 -*-
"""
Created on Thu May 28 00:26:24 2015

@author: Administrator
"""

import os
import datetime
import time
from string import *
def sumup (a , ref):
    print "Positive :" , a.count(ref[0])
    print "Negetive :" ,a.count(ref[1])
    print "Neutral  :" , a.count(ref[2])
    return

#def getfiles (d as os.dire):
#   return  d.
location ="c:\\ABCDEFG\output"
inputloc = "c:\\ABCDEFG\input"
#print str.format(datetime.date)

#process the input file
for files in  os.listdir(inputloc):
# do logic here
    fname = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    outputpath  = 'c:\\ABCDEFG\\output\\' +fname+'_output.txt'
    print outputpath
    outputfile = open(outputpath, "w")

'''

fname = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())

#print date(‘%Y-%m-%d %H:%M:%S’)

outputpath  = 'c:\\ABCDEFG\\output\\' +fname+'_output.txt'
print outputpath

outputfile = open(outputpath, "w")
outputlist = ["Positive", "Negative", "Neutral"]



#print 'fileName\t\tPos\tNeg\tNeu'
for files in  os.listdir("c:\\ABCDEFG\output"):
    #print files
    with open(location+"\\"+files, "r") as ins:
        
        array = []
        for line in ins:
            array.append(line.rstrip('\n'))
    outputfile.write( '%5s\t%s\t%s\t%s\n' %(files ,array.count(outputlist[0]),array.count(outputlist[1]),array.count(outputlist[2])))
    
#    sumup(array, outputlist)   
#    outputfile.writelines("%s\t%s" % files % array.count(outputlist[0]) )

'''

outputfile.close()