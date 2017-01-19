import ast
import re
import sys
import string
import os.path

# needed for identifying emotion with highest score
import operator
from operator import itemgetter

# needed for MySQL
import mysql.connector
from mysql.connector import MySQLConnection, Error, connect, errorcode

# NLTK, language analysis
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import *
# import nltk.classify.util, nltk.metrics
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


# GENSIM, language analysis
from gensim.summarization import summarize
import tweepy
from tweepy import OAuthHandler, AppAuthHandler

# ********LEXICON DATABASE ACCESS***********

with open(os.path.dirname(__file__) + '../.env') as secrets:

	lies = dict(ast.literal_eval(secrets.read()))
	
	SECRET_KEY = lies['SECRET_KEY']
	USER_NAME = lies['USER_NAME']
	DATABASE_NAME = lies['DATABASE_NAME']
	DATABASE_KEY = lies['DATABASE_KEY']
	CONSUMER_KEY = lies['CONSUMER_KEY']
	CONSUMER_SECRET = lies['CONSUMER_SECRET']
	ACCESS_TOKEN = lies['ACCESS_TOKEN']
	ACCESS_SECRET =	lies['ACCESS_SECRET']
	CALLBACK_URL = lies['CALLBACK_URL']
	HOST = lies['HOST']

# *******************
TWITTER_AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
TWITTER_AUTH.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
AUTHORIZED_USER = tweepy.API(TWITTER_AUTH, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



# *******************
tokenizer = TweetTokenizer()

symbol_sentence = '@POTUS Thank you for your service.  You were amazing! <3'

test_sentence = 'abandon the abacus show some courage find yourself be a man'

punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '...', '…', '@']

# ********************

# symbol_tokens = tokenizer.tokenize(test_sentence) #includes @ and # etc as part of a word

clean_symbol_tokens = word_tokenize(symbol_sentence) 

# print(clean_symbol_tokens)

stop_words = set(stopword_list)

# print(stop_words)



# filtered_sentence = [w for w in symbol_tokens if not w in stop_words]

# filtered_sentence = []

# for w in symbol_tokens:
#     if w not in stop_words:
#         filtered_sentence.append(w)

# print(symbol_tokens)
# print(filtered_sentence)



filtered_sentence = [w for w in clean_symbol_tokens if not w in stop_words]

filtered_sentence = []

for w in clean_symbol_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

# print(clean_symbol_tokens)
# print(filtered_sentence)



def query_emolex(host, database, user, password, tweet_word):
	cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
	cursor = cnx.cursor(dictionary=True)
	tweet_word = mysql_real_escape_string(tweet_word)

	query = cnx.escape_string("SELECT w.word, e.emotion, w.count, wes.score, wes.word_id, wes.emotion_id, w.id, e.id FROM words w JOIN word_emotion_score wes ON wes.word_id = w.id JOIN emotions e ON e.id = wes.emotion_id WHERE w.word = %s")

	cursor.execute(query, [tweet_word])

	results = cursor.fetchall()

	emotion_list = []

	for emotion in results:
		average_score = emotion['score']/emotion['count']
		emotion_w_score = (emotion['emotion'], average_score)
		emotion_list.append(emotion_w_score)

	return emotion_list
	# print(emotion_list)

	cursor.close()
	cnx.close()



def find_strongest_emotion_for_word(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet_word):

	emotion_list = query_emolex(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet_word)
	if not emotion_list:
		return []
	highest_scoring_emotion = max(emotion_list, key=itemgetter(1))[0]
	return highest_scoring_emotion



def find_strongest_emotions_in_tweet(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, word_list):
	emotion_list = []
	
	for word in word_list:
		highest_scoring_emotion = find_strongest_emotion_for_word(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, word)
		emotion_list.append(highest_scoring_emotion)
	
	return emotion_list
		# print(emotion_list)




# print(find_strongest_emotions_in_tweet(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, rose_test_tweet))


with open('rose_test_raw.txt') as raw_tweets:
	tweets = raw_tweets.read().split('\n')
	clean_tweets = []

## CRITICAL!  IMPORTANT!  DB BREAKS OTHERWISE!
	regex = re.compile('[^a-zA-Z/\s]')

	for tweet in tweets:
		print(tweet)
		clean_tweet = regex.sub('', tweet)
		# print(clean_tweet)
		tweet_tokens = word_tokenize(tweet)

		filtered_tweet = [w for w in tweet_tokens if not w in stop_words]
		filtered_tweet = []

		for w in tweet_tokens:
			if w not in stop_words:
				filtered_tweet.append(w)

		clean_tweets.append(filtered_tweet)

# print(clean_tweets[3])


# # print(find_strongest_emotions_in_tweet(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY,clean_tweets[3]))

# found_emotions = []

for tweet in clean_tweets:
	print(tweet)
	print(find_strongest_emotions_in_tweet(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet))
# 	# found_emotions.append(results)

print(found_emotions)

