import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import *
import ast
import re
import collections
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier


import itertools
from nltk.collocations import BigramCollocationFinder

from nltk.corpus import stopwords



first_pass = open('NRC-emolex-short-practice.txt').read().strip().replace('\t', " ").replace(" ", ",").split('\n')

# first_pass = open('NRC-emolex-short-practice.txt').read().strip().split('\n')

# print(first_pass)

second_pass = list(map(lambda w:w.split(','), first_pass))

print(second_pass[0])




anger = {}
anticipation = {}
disgust = {}
fear = {}
joy = {}
negative = {}
positive = {}
sadness = {}
surprise = {}
trust = {}

anger_array = []
anticipation_array = []
disgust_array = []
fear_array = []
joy_array = []
negative_array = []
positive_array = []
sadness_array = []
surprise_array = []
trust_array = []

word_array = ['abandoned', 'anger', '1']

def third_pass(word_array, sentiment_array):
	if word_array[-1] == "1":
		sentiment_array.append(word_array[0])

third_pass(word_array, anger_array)

print(anger_array)
		
anger.update(anger_array)
# anticipation.update(anticipation_array)
# disgust.update(disgust_array)
# fear.update(fear_array)
# joy.update(joy_array)
# negative.update(negative_array)
# positive.update(positive_array)
# sadness.update(sadness_array)
# surprise.update(surprise_array)
# trust.update(trust_array)	

print(anger)

def fourthpass(word_array, sentiment_array):
	for array in word_array:
		third_pass(array, sentiment_array)


# fourthpass = fourthpass(second_pass, anger_array)
# print(anger_array)
# for string in first_pass:
# 	if string[-1] == "1":
# 		print('yes')
# 	else:
# 		print('no')

# test_word = 'aback\tanger\t0'
# print(test_word)

# second_pass = test_word.split('\t', 1)[0]

# # print(second_pass)

# third_pass = test_word.split('\t', 2)

# print(third_pass)
# # print(third_pass[1])

# hash = {}

# # print(type(third_pass[0]))

# # hash[third_pass[0]] = third_pass[1]

# # hash[str(third_pass[0])][str(third_pass[1])]
# # print(hash)

# array = []
# set = {}

# def assignvalue(word, set):
# 	default = 0
	
# 	if word[-1] == "1":
# 		key = word.split('\t', 2)[0]
# 		value = word.split('\t', 2)[1]

		

# 		# dictionary.setdefault(key, default)

# 		# if value == "anger":
# 		# 	dictionary[key] += 1
# 		# if value == "anticipation":
# 		# 	dictionary[key] += 2
# 		# if value == "disgust":
# 		# 	dictionary[key] += 4
# 		# if value == "fear":
# 		# 	dictionary[key] += 8
# 		# if value == "joy":
# 		# 	dictionary[key] += 16
# 		# if value == "negative":
# 		# 	dictionary[key] += 32
# 		# if value == "positive":
# 		# 	dictionary[key] += 64
# 		# if value == "sadness":
# 		# 	dictionary[key] += 128
# 		# if value == "surprise":
# 		# 	dictionary[key] += 256
# 		# if value == "trust":
# 		# 	dictionary[key] += 512



# for wordblob in first_pass:
# 	assignvalue(wordblob, dictionary)

# print(dictionary)

test_sentence = 'abandon the abacus'

sentence_hash = {"anger": 0, "anticipation": 0, "disgust": 0, "fear": 0, "joy": 0, "negative": 0, "positive": 0, "sadness": 0, "surprise": 0, "trust": 0}

def fifthpass(word, set):
	if set[word]:
		return True
	else:
		return False

def sixthpass(sentence, set1, set2, set3, set4, set5, set6, set7, set8, set9, set10): 
	sentence_hash = {"anger": 0, "anticipation": 0, "disgust": 0, "fear": 0, "joy": 0, "negative": 0, "positive": 0, "sadness": 0, "surprise": 0, "trust": 0}

	for word in sentence:
		if set1[word]:
			sentence_hash['anger'] += 1
		if set2[word]:
			sentence_hash['anticipation'] += 1
		if set3[word]:
			sentence_hash['disgust'] += 1
		if set4[word]:
			sentence_hash['fear'] += 1
		if set5[word]:
			sentence_hash['joy'] += 1
		if set6[word]:
			sentence_hash['negative'] += 1
		if set7[word]:
			sentence_hash['positive'] += 1
		if set8[word]:
			sentence_hash['sadness'] += 1
		if set9[word]:
			sentence_hash['surprise'] += 1
		if set10[word]:
			sentence_hash['trust'] += 1
	return sentence_hash

seventhpass = sixthpass(test_sentence, )
# 		dictionary.setdefault(word, 0)

# 		if dictionary[word] == 'anger':
# 			sentence_hash['anger'] += 1
# 		if dictionary[word] == 'anticipation':
# 			sentence_hash['anticipation'] += 1
# 		if dictionary[word] =='disgust':
# 			sentence_hash['disgust'] += 1
# 		if dictionary[word] == 'fear':
# 			sentence_hash['fear'] += 1
# 		if dictionary[word] == 'joy':
# 			sentence_hash['joy'] += 1
# 		if dictionary[word] == 'negative':
# 			sentence_hash['negative'] += 1
# 		if dictionary[word] == 'positive':
# 			sentence_hash['positive'] += 1
# 		if dictionary[word] == 'anticipation':
# 			sentence_hash['sadness'] += 1
# 		if dictionary[word] == 'anticipation':
# 			sentence_hash['surprise'] += 1
# 		if dictionary[word] == 'anticipation':
# 			sentence_hash['trust'] += 1

# 	return sentence_hash



# print(checksentence(test_sentence, dictionary))
















# # sentence_hash = {"anger": 0, "anticipation": 0, "disgust": 0, "fear": 0, "joy": 0, "negative": 0, "positive": 0, "sadness": 0, "surprise": 0, "trust": 0}

# # anger = 1
# # anticipation = 2
# # disgust = 4
# # fear = 8
# # joy = 16
# # negative = 32
# # positive = 64
# # sadness = 128
# # surprise = 256
# # trust = 512

# def checkdictionary(sentence, dictionary):
# 	default = 0
# 	sentence_hash = {"anger": 0, "anticipation": 0, "disgust": 0, "fear": 0, "joy": 0, "negative": 0, "positive": 0, "sadness": 0, "surprise": 0, "trust": 0}

# 	anger = 1
# 	anticipation = 2
# 	disgust = 4
# 	fear = 8
# 	joy = 16
# 	negative = 32
# 	positive = 64
# 	sadness = 128
# 	surprise = 256
# 	trust = 512

# 	for word in sentence:
# 		dictionary.setdefault(word, default)

# 		if dictionary[word]:
# 			value = dictionary[word]

# 			if value - anger >= 0:
# 				sentence_hash['anger'] += 1
# 			if value - anticipation >= 0:
# 				sentence_hash['anticipation'] += 1
# 			if value - disgust >= 0:
# 				sentence_hash['disgust'] += 1
# 			if value - fear >= 0:
# 				sentence_hash['fear'] += 1
# 			if value - joy >= 0:
# 				sentence_hash['joy'] += 1
# 			if value - negative >= 0:
# 				sentence_hash['negative'] += 1
# 			if value - positive >= 0:
# 				sentence_hash['positive'] += 1
# 			if value - sadness >= 0:
# 				sentence_hash['sadness'] += 1
# 			if value - surprise >= 0:
# 				sentence_hash['surprise'] += 1
# 			if value - trust >= 0:
# 				sentence_hash['trust'] += 1

# 	return sentence_hash


# # print(checkdictionary(test_sentence, dictionary))

#  