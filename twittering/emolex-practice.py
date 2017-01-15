import ast
import re
import sys
import re
import string
import json
import os.path

import collections
from collections import Counter
import operator
from operator import itemgetter

import mysql.connector
from mysql.connector import MySQLConnection, Error, connect, errorcode
# import mysqldb.converters
# from mysqldb.converters import conversions
# conv=converters.conversions.copy()
# conv[246]=float    # convert decimals to floats
# conv[10]=str 

# NLTK
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import *
# import nltk.classify.util, nltk.metrics
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

# GENSIM
from gensim.summarization import summarize

import itertools

# ********LEXICON DATABASE ACCESS***********

with open(os.path.dirname(__file__) + '../.env') as secrets:

	lies = dict(ast.literal_eval(secrets.read()))
	USER_NAME = lies['USER_NAME']
	DATABASE_NAME = lies['DATABASE_NAME']
	DATABASE_KEY = lies['DATABASE_KEY']
	HOST = lies['HOST']

# *******************

# *******************
tokenizer = TweetTokenizer()

test_sentence = 'abandon the abacus bazooka'

punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '...', '…']
# *******************


def prep_tweets(textfile):
	
	first_step = open(textfile).read().strip().replace('\t', " ").replace(" ", ",").split('\n')
	tweet_list = list(map(lambda w:w.split(','), first_step))
	
	return tweet_list



def process(text, tokenizer=TweetTokenizer(), stopwords=[]):

	text = text.lower()
	tokens = tokenizer.tokenize(text)

	return [tok for tok in tokens if tok not in stopword_list and not tok.isdigit()]


test_list = process(test_sentence, tokenizer=TweetTokenizer(), stopwords=stopword_list)



def query_lexicon(host, database, user, password, tweet_word):
	cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
	cursor = cnx.cursor()

	query = ('SELECT word_id, word ')

	cursor.execute(query)

	for (emotions) in cursor:
		print(emotions)

	cursor.close()
	cnx.close()	




	# 	# anger = float(anger[1])
	# 	# anticipation = float(anticipation[1])
	# 	# disgust = float(disgust[1])		
	# 	# fear = float(fear[1])	
	# 	# joy = float(joy[1])
	# 	# sadness = float(sadness[1])
	# 	# surprise = float(surprise[1])
	# 	y = float(trust[1])

	# emotion_set = {'anger': anger, 'anticipation': anticipation, 'disgust': disgust, 'fear': fear, 'joy': joy, 'sadness': sadness, 'surprise': surprise, 'trust': trust}

	# print(y)

	cursor.close()
	cnx.close()

# connect_database(USER_NAME, DATABASE_KEY, HOST, DATABASE_NAME)

# query_emolex(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, 'death')

def query_emolex(host, database, user, password, tweet_word):
	cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
	cursor = cnx.cursor(dictionary=True)
	# cursor = cnx.cursor()

	query = ("SELECT w.word, e.emotion, w.count, wes.score, wes.word_id, wes.emotion_id, w.id, e.id FROM words w JOIN word_emotion_score wes ON wes.word_id = w.id JOIN emotions e ON e.id = wes.emotion_id WHERE w.word = '%s'" % tweet_word)

	cursor.execute(query)

	patch = cursor.fetchall()

	wheelbarrow = []

	for cabbage in patch:
		average_score = cabbage['score']/cabbage['count']
		green = (cabbage['emotion'], average_score)
		wheelbarrow.append(green)

	return wheelbarrow


	cursor.close()
	cnx.close()



# print(query_emolex(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, 'baby'))

def find_strongest_emotion(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet_word):

	litter = query_emolex(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet_word)

	pick = max(litter, key=itemgetter(1))[0]
	print(pick)


find_strongest_emotion(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, 'baby')





def connect_database(user, password, host, database):
	try:
		cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)

		if cnx.is_connected():
			print('connection established.')
		else:
			print('connection failed.')
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your username or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cnx.close()

# connect_database(USER_NAME, DATABASE_KEY, HOST, DATABASE_NAME)

# cnx = mysql.connector.connect(user=USER_NAME, password=DATABASE_KEY, host=HOST, database=DATABASE_NAME)

# cursor = cnx.cursor()

# query = ("SELECT AVG(joy) FROM twittering.emolex WHERE word = 'baby'")

# tweet_word = 'rabbit'

# cursor.execute(query)

# for (joy) in cursor:
# 	print("Joy: {}".format(joy)) 
# cursor.close()
# cnx.close()





def sixthpass(sentence_array, anger_set, anticipation_set, disgust_set, fear_set, joy_set, negative_set, positive_set, sadness_set, surprise_set, trust_set):
	
	sentence_hash = {"anger": 0, "anticipation": 0, "disgust": 0, "fear": 0, "joy": 0, "negative": 0, "positive": 0, "sadness": 0, "surprise": 0, "trust": 0}

	for word in sentence_array:
		# print(word)
		if word in anger_set:
			sentence_hash['anger'] += 1
		if word in anticipation_set:
			sentence_hash['anticipation'] += 1
		if word in disgust_set:
			sentence_hash['disgust'] += 1
		if word in fear_set:
			sentence_hash['fear'] += 1
		if word in joy_set:
			sentence_joy['joy'] += 1
		if word in negative_set:
			sentence_hash['negative'] += 1
		if word in positive_set:
			sentence_hash['positive'] += 1
		if word in sadness_set:
			sentence_hash['sadness'] += 1
		if word in surprise_set:
			sentence_hash['surprise'] += 1
		if word in trust_set:
			sentence_hash['trust'] += 1
	return sentence_hash


important_punctuation = '¯\\_(ツ)_/¯'

