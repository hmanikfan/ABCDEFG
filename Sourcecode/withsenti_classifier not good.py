# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#from senti_classifier import senti_classifier

import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
import sring


inputpath  = 'D:\SourceCode\inputsample.txt'
outputpath  = 'D:\SourceCode\outputsample1.txt'

input_file = open(inputpath, 'r')
output_file = open(outputpath, "w")

lines = input_file.readlines()

#print (content)

for line in lines:
    for sentence in sent_tokenize (line):
        print pos_tag(word_tokenize(sentence))
        
        
        
        
        '''
for line in lines:
    pos_score, neg_score = senti_classifier.polarity_scores(line)
    if (pos_score > neg_score):
        print 1
        output_file.write ("Positive")
    elif (pos_score < neg_score):
        print 2
        output_file.write ("Negative")
    else:
        print 3
        output_file.write ("Neutral"+"\n")


output_file.close()
input_file.close()

'''