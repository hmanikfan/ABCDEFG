import sys
import csv
import nltk
from nltk.corpus import wordnet
import re
import codecs
import pprint
from nltk.wsd import lesk
#from sentiwordnet import SentiWordNetCorpusReader, SentiSynset
from nltk.corpus import sentiwordnet as swn


def tweet_dict(twitterData):  
    ''' (file) -> list of dictionaries
    This method should take your .csv
    file and create a list of dictionaries.
    '''
    twitter_list_dict = []    
    twitterfile = open(twitterData)
    twitterreader = csv.reader(twitterfile)
    for line in twitterreader:
        twitter_list_dict.append(line[0])
    return twitter_list_dict

# return true if a string ia a stopword
def is_stopword(string):
    if string.lower() in nltk.corpus.stopwords.words('english'):
        return True
    else:
        return False

    # return true if a string is punctation    
def is_punctuation(string):
    for char in string:
        if char.isalpha() or char.isdigit():
            return False
    return True

# Translation from nltk to Wordnet (words tag) (code)
def wordnet_pos_code(tag):
    if tag.startswith('NN'):
        return wordnet.NOUN
    elif tag.startswith('VB'):
        return wordnet.VERB
    elif tag.startswith('JJ'):
        return wordnet.ADJ
    elif tag.startswith('RB'):
        return wordnet.ADV
    else:
        return ''

    
# Translation from nltk to Wordnet (words tag) (label)
def wordnet_pos_label(tag):
    if tag.startswith('NN'):
        return "Noun"
    elif tag.startswith('VB'):
        return "Verb"
    elif tag.startswith('JJ'):
        return "Adjective"
    elif tag.startswith('RB'):
        return "Adverb"
    else:
        return tag
    

""" input -> a sentence 
    otput -> sentence in which each words is enriched of -> lemma, wordnet_pos, wordnet_definitions 

"""
def wordnet_definitions(sentence):
    wnl = nltk.WordNetLemmatizer()
    for token in sentence:
        word = token['word']
        wn_pos = wordnet_pos_code(token['pos'])
        if is_punctuation(word):
            token['punct'] = True
        elif is_stopword(word):
            pass
        elif len(wordnet.synsets(word, wn_pos)) > 0:
            token['wn_lemma'] = wnl.lemmatize(word.lower())
            token['wn_pos'] = wordnet_pos_label(token['pos'])
            defs = [sense.definition for sense in wordnet.synsets(word, wn_pos)]
            token['wn_def'] = "; \n".join(str(v) for v in defs) 
        else:
            pass
    return sentence


#Tokenization

def tag_tweet(tweet):    
    sents = nltk.sent_tokenize(tweet)
    sentence = []
    for sent in sents:
        tokens = nltk.word_tokenize(sent)
        tag_tuples = nltk.pos_tag(tokens)
        for (string, tag) in tag_tuples:
            token = {'word':string, 'pos':tag}            
            sentence.append(token)    
    return sentence


"""
# WSD

def word_sense_disambiguate(word, wn_pos, tweet):
    senses = wordnet.synsets(word, wn_pos)
    if len(senses) >0:
        cfd = nltk.ConditionalFreqDist(
               (sense, def_word)
               for sense in senses
               for def_word in sense.definition.split()
               if def_word in tweet)
        best_sense = senses[0] # start with first sense
        for sense in senses:
            try:
                if cfd[sense].max() > cfd[best_sense].max():
                    best_sense = sense
            except: 
                pass                
        return best_sense
    else:
        return None
"""
#swn_filename = 'D:/SentiWordNet_3.0.0.txt'
#swn = SentiWordNetCorpusReader(swn_filename)

#sentiment = SentiWordNetCorpusReader("D:/SentiWordNet_3.0.0.txt")

#review = "I bought this tablecloth in the taupe color for Thanksgiving dinner entertaining and was a little hesitant of what I would get for such a reasonable price. It washed well and didn't even need pressing after coming out of the dryer. The color worked out great with my gold-trimmed Lenox placesettings and the tablecloth was of a nice weight - not too flimsy yet not too heavy either. I'm pleased with this purchase and may order another in a smaller size for use now that the leaf is out of the table!"


review = "I took the day off yesterday for the installation, whole family was around and the technician did not show up. How do I cancel the service now?"

#review = "Blazing fast internet speeds... I'm blown away"



inputpath  = 'D:\SourceCode\inputsample.txt'
outputpath  = 'D:\SourceCode\outputsample1.txt'

input_file = open(inputpath, 'r')
output_file = open(outputpath, "w")

lines = input_file.readlines()


#a = wordnet_definitions(tag_tweet(lines))
#print a

pos_score_tre=0
neg_score_tre=0
threshold = 0.75
count = 0
count_tre = 0

"""
Conversion from plain text to SentiWordnet scores
"""


for line in lines:
    obj_score = 0 # object score 
    pos_score=0 # positive score
    neg_score=0 #negative score
    for word in wordnet_definitions(tag_tweet(line)):
        if 'punct' not in word :
            
            #sense = word_sense_disambiguate(word['word'], wordnet_pos_code(word['pos']), review)
            #lesk(sent, word, pos))
            sense = lesk (review,word['word'], wordnet_pos_code(word['pos']))
            #print "1",sense
            if sense is None:
                sense = lesk (review,word['word'])
                #print "2",sense
            if sense is not None:
                #sent = sentiment.senti_synset(sense.name)
                sent = swn.senti_synset(sense.name())
                #print "3" , sent
                if sent is not None and sent.obj_score() <> 1:
                    obj_score = obj_score + float(sent.obj_score())
                    pos_score = pos_score + float(sent.pos_score())
                    neg_score = neg_score + float(sent.neg_score())
                
    print pos_score,neg_score,obj_score ,  pos_score-neg_score

"""
            # Extraction of the scores
            if sent is not None and sent.obj_score() <> 1:
                obj_score = obj_score + float(sent.obj_score())
                pos_score = pos_score + float(sent.pos_score())
                neg_score = neg_score + float(sent.neg_score())
                count=count+1
                print str(sent.pos_score())+ " - "+str(sent.neg_score())+ " - "+ str(sent.obj_score())+" - "+sent.synset.name()
                if sent.obj_score() < threshold:
                    pos_score_tre = pos_score_tre + float(sent.pos_score())
                    neg_score_tre = neg_score_tre + float(sent.neg_score())
                    count_tre=count_tre+1
print review

#Evaluation by different methods

avg_pos_score=0
avg_neg_score=0
avg_neg_score_tre=0
avg_neg_score_tre=0

#2

if count <> 0:
    
    avg_pos_score=pos_score/count
    avg_neg_score=neg_score/count

#3

if count_tre <> 0:
    avg_pos_score_tre=pos_score_tre/count_tre
    avg_neg_score_tre=neg_score_tre/count_tre

#pint results
#1
print "pos_total : "+str(pos_score)+" - neg_ total: "+str(neg_score)+" - count : "+str(count)+" -> "+(" positivo " if pos_score > neg_score else ("negativo" if pos_score < neg_score else "neutro"))
#2
print "(AVG) pos : "+str(avg_pos_score)+" - (AVG) neg : "+str(avg_neg_score)+" -> "+(" positivo " if avg_pos_score > avg_neg_score else ("negativo" if avg_pos_score < avg_neg_score else "neutro"))
#3
if count_tre > 0:
    print "(AVG_TRE) pos : "+str(avg_pos_score_tre)+" - (AVG_TRE) neg : "+str(avg_neg_score_tre)+" -> "+(" positivo " if avg_pos_score_tre > avg_neg_score_tre else ("negativo" if avg_pos_score_tre < avg_neg_score_tre else "neutro"))
print ""

"""