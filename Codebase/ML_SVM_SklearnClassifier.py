import re, math, collections, itertools, os
import datetime
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import pandas as pd
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from nltk.collocations import BigramCollocationFinder


POLARITY_DATA_DIR = os.path.join('c:/abcdefg/polarity/')
RT_POLARITY_POS_FILE = os.path.join(POLARITY_DATA_DIR, 'rt-polarity-pos.txt')
RT_POLARITY_NEG_FILE = os.path.join(POLARITY_DATA_DIR, 'rt-polarity-neg.txt')
RT_INPUT_NEG_FILE = os.path.join(POLARITY_DATA_DIR, 'HackathonInput.txt')
RT_INPUT_POS_FILE = os.path.join(POLARITY_DATA_DIR, 'posSample.txt')

df = pd.DataFrame()
#this function takes a feature selection mechanism and returns its performance in a variety of metrics
def evaluate_features(feature_select):
    posFeatures = []
    negFeatures = []
    inposFeatures = []
    innegFeatures = []
	#http://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
	#breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
    with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
        for i in posSentences:
            posWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            posWords = [feature_select(posWords), 'pos']
            posFeatures.append(posWords)
    with open(RT_POLARITY_NEG_FILE, 'r') as negSentences:
        for i in negSentences:
            negWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            negWords = [feature_select(negWords), 'neg']
            negFeatures.append(negWords)
    """
    with open(RT_INPUT_POS_FILE, 'r') as posSentences:
        for i in posSentences:
            inposWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            inposWords = [feature_select(inposWords), 'pos']
            inposFeatures.append(inposWords)
    """
    with open(RT_INPUT_NEG_FILE, 'r') as negSentences:
        for i in negSentences:
            innegWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            innegWords = [feature_select(innegWords), 'neg']
            innegFeatures.append(innegWords)
   
	#selects 3/4 of the features to be used for training and 1/4 to be used for testing
	#posCutoff = int(math.floor(len(posFeatures)*3/4))
	#negCutoff = int(math.floor(len(negFeatures)*3/4))
    trainFeatures = posFeatures + negFeatures
    testFeatures = innegFeatures #+ inposFeatures
      
    	#trains a Naive Bayes Classifier
    #classifier = SklearnClassifier(BernoulliNB()).train(trainFeatures)	
    classifier = SklearnClassifier(SVC(probability=True), sparse=False).train(trainFeatures)	
    
    	#initiates referenceSets and testSets
    referenceSets = collections.defaultdict(set)
    testSets = collections.defaultdict(set)	

    fileOutput ={'key':[],'pos':[],'neg':[]}
	#puts correctly labeled sentences in referenceSets and the predictively labeled version in testsets
    for i, (features, label) in enumerate(testFeatures):
        #print features , label
        referenceSets[label].add(i)
        predicted = classifier.prob_classify_many(features)
        print "\n" 
        #print predicted
        for item in predicted:
            fileOutput['key'].append(i)
            fileOutput['pos'].append(item.prob("pos"))
            fileOutput['neg'].append(item.prob("neg"))
        #posValues =  predicted.prob("pos") 
        #negValues = predicted.prob("neg") 
        fileOutput.values()
        #testSets[predicted].add(i)
        #print i
        #print testSets[predicted]
    return fileOutput
"""
    #prints metrics to show how well the feature selection did
    print 'train on %d instances, test on %d instances' % (len(trainFeatures), len(testFeatures))
    print 'accuracy:', nltk.classify.util.accuracy(classifier, testFeatures)
    print 'pos precision:', nltk.metrics.precision(referenceSets['pos'], testSets['pos'])
    print 'pos recall:', nltk.metrics.recall(referenceSets['pos'], testSets['pos'])
    print 'neg precision:', nltk.metrics.precision(referenceSets['neg'], testSets['neg'])
    print 'neg recall:', nltk.metrics.recall(referenceSets['neg'], testSets['neg'])
    #classifier.show_most_informative_features(10)
"""
    
#creates a feature selection mechanism that uses all words
def make_full_dict(words):
	return dict([(word, True) for word in words])

#tries using all words as the feature selection mechanism
#print 'using all words as features'
#evaluate_features(make_full_dict)

#scores words based on chi-squared test to show information gain (http://streamhacker.com/2010/06/16/text-classification-sentiment-analysis-eliminate-low-information-features/)
def create_word_scores():
	#creates lists of all positive and negative words
	posWords = []
	negWords = []
	with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
		for i in posSentences:
			posWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			posWords.append(posWord)
	with open(RT_POLARITY_NEG_FILE, 'r') as negSentences:
		for i in negSentences:
			negWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			negWords.append(negWord)
	posWords = list(itertools.chain(*posWords))
	negWords = list(itertools.chain(*negWords))

	#build frequency distibution of all words and then frequency distributions of words within positive and negative labels
	word_fd = FreqDist()
	cond_word_fd = ConditionalFreqDist()
	for word in posWords:
		word_fd[word.lower()] += 1
		cond_word_fd['pos'][word.lower()] += 1
	for word in negWords:
		word_fd[word.lower()] += 1
		cond_word_fd['neg'][word.lower()] += 1

	#finds the number of positive and negative words, as well as the total number of words
	pos_word_count = cond_word_fd['pos'].N()
	neg_word_count = cond_word_fd['neg'].N()
	total_word_count = pos_word_count + neg_word_count

	#builds dictionary of word scores based on chi-squared test
	word_scores = {}
	for word, freq in word_fd.iteritems():
		pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
		neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
		word_scores[word] = pos_score + neg_score

	return word_scores

#finds word scores
word_scores = create_word_scores()

#finds the best 'number' words based on word scores
def find_best_words(word_scores, number):
	best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
	best_words = set([w for w, s in best_vals])
	return best_words

#creates feature selection mechanism that only uses best words
def best_word_features(words):
	return dict([(word, True) for word in words if word in best_words])

#classifier = Pipeline([('vectorizer', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', OneVsRestClassifier(SVC(kernel='rbf')))])

def best_bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
	print "bigrams in da house"

	bigram_finder = BigramCollocationFinder.from_words(words)
	bigrams = bigram_finder.nbest(score_fn, n)
	d = dict([(bigram, True) for bigram in bigrams])
	d.update(best_word_features(words))
	return d
 
dp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
#outputpath  = 'D:\SourceCode\outputsamplebay1.txt'
#outputpath  = 'D:\\SourceCode\\Output_NBC_'+ dp + '.txt'
outputpath  = 'C:\\ABCDEFG\\output\\ABCDEFG_MLSVM_'+ dp + '.txt'
#outputpath  = 'D:\SourceCode\outputsamplesvm1.txt'


output_file = open(outputpath, 'w')

#numbers of features to select
#numbers_to_test = [10, 100, 1000, 10000, 15000]
numbers_to_test = [1000]
#tries the best_word_features mechanism with each of the numbers_to_test of features
for num in numbers_to_test:
    print 'evaluating best %d word features' % (num)
    best_words = find_best_words(word_scores, num)
    output = evaluate_features(best_word_features)
    df = pd.DataFrame(output)
    print df
    df['diff'] = df['pos'] - df['neg']
    diff = df['diff'].tolist()
    for score in diff:
        if score > 0:
            op = 'Positive'  + '\n'
        elif score < 0:
            op = 'Negative' + '\n'
        else:
            op = 'Neutral' + '\n'
            
        output_file.writelines(op)

    #print pd.DataFrame(output.items(), columns=['key','pos', 'neg'])


