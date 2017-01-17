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

test_sentence = 'abandon the abacus show some courage find yourself be a man'

punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '...', '…']
# *******************




# def prep_tweets(textfile):
	
# 	first_step = open(textfile).read().strip().replace('\t', " ").replace(" ", ",").split('\n')
# 	tweet_list = list(map(lambda w:w.split(','), first_step))
	
# 	return tweet_list



# def process(text, tokenizer=TweetTokenizer(), stopwords=[]):

# 	text = text.lower()
# 	tokens = tokenizer.tokenize(text)

# 	return [tok for tok in tokens if tok not in stopword_list and not tok.isdigit()]


# test_list = process(test_sentence, tokenizer=TweetTokenizer(), stopwords=stopword_list)

# rose_tweets = open('rose_test_raw.txt').read().split('\n')

# rose_test_tweet = process(rose_tweets[0])

# # print(rose_tweets[0])
# # print(rose_test_tweet)


# def query_emolex(host, database, user, password, tweet_word):
# 	cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
# 	cursor = cnx.cursor(dictionary=True)


# 	query = ("SELECT w.word, e.emotion, w.count, wes.score, wes.word_id, wes.emotion_id, w.id, e.id FROM words w JOIN word_emotion_score wes ON wes.word_id = w.id JOIN emotions e ON e.id = wes.emotion_id WHERE w.word = '%s'" % tweet_word)

# 	cursor.execute(query)

# 	results = cursor.fetchall()

# 	emotion_list = []

# 	for emotion in results:
# 		average_score = emotion['score']/emotion['count']
# 		emotion_w_score = (emotion['emotion'], average_score)
# 		emotion_list.append(emotion_w_score)

# 	return emotion_list


# 	cursor.close()
# 	cnx.close()



# # print(query_emolex(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, 'richest'))

# def find_strongest_emotion_for_word(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet_word):

# 	emotion_list = query_emolex(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet_word)
# 	if not emotion_list:
# 		return []
# 	highest_scoring_emotion = max(emotion_list, key=itemgetter(1))[0]
# 	return highest_scoring_emotion


# # print(find_strongest_emotion_for_word(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, 'man'))


# def find_strongest_emotions_in_tweet(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, word_list):
# 	emotion_list = []
	
# 	for word in word_list:
# 		highest_scoring_emotion = find_strongest_emotion_for_word(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, word)
# 		emotion_list.append(highest_scoring_emotion)
	
# 	return emotion_list




# # print(find_strongest_emotions_in_tweet(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, rose_test_tweet))

# # test_run_tweet = find_strongest_emotions_in_tweet(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, rose_test_tweet)


# def connect_database(user, password, host, database):
# 	try:
# 		cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)

# 		if cnx.is_connected():
# 			print('connection established.')
# 		else:
# 			print('connection failed.')
# 	except mysql.connector.Error as err:
# 		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
# 			print("Something is wrong with your username or password")
# 		elif err.errno == errorcode.ER_BAD_DB_ERROR:
# 			print("Database does not exist")
# 		else:
# 			print(err)
# 	else:
# 		cnx.close()





# def show_top_emotion(emotion_array):
	
# 	emotion_hash = {"anger": 0, "anticipation": 0, "disgust": 0, "fear": 0, "joy": 0, "negative": 0, "positive": 0, "sadness": 0, "surprise": 0, "trust": 0}

# 	for emotion in emotion_array:
# 		# print(emotion)
# 		if emotion == 'anger':
# 			emotion_hash['anger'] += 1
# 		if emotion == 'anticipation':
# 			emotion_hash['anticipation'] += 1
# 		if emotion == 'disgust':
# 			emotion_hash['disgust'] += 1
# 		if emotion == 'fear':
# 			emotion_hash['fear'] += 1
# 		if emotion == 'joy':
# 			emotion_hash['joy'] += 1
# 		if emotion == 'sadness':
# 			emotion_hash['sadness'] += 1
# 		if emotion == 'surprise':
# 			emotion_hash['surprise'] += 1
# 		if emotion == 'trust':
# 			emotion_hash['trust'] += 1
# 	return emotion_hash

# # print(test_sentence)
# # print(show_top_emotion(test_run_tweet))
# # print(rose_test_tweet)
# # print(show_top_emotion(rose_test_tweet))

# def test_get_tweets(AUTHORIZED_USER, target_handle, number_of_tweets):			
# 	rawtweepy = AUTHORIZED_USER.user_timeline(screen_name=target_handle, count=number_of_tweets)

# 	tweets = list(map(lambda t:t.text, rawtweepy))	
# 	return tweets

# def test_classify(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweets):

# 	tweet_emotions = []

# 	for tweet in tweets:
# 		tweet_emotions.append(tweet)

# 		tweet_words = process(tweet)
# 		print(tweet_words)
# 		# emotions_list = find_strongest_emotions_in_tweet(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet_words)
# 		# print(emotions_list)
# 		# tweet_emotions.append(emotions_list)
# 		tweet_emotions.append(tweet_words)

# 	return tweet_emotions

# # testing_tweets = test_get_tweets(AUTHORIZED_USER, 'RedSquirrelious', 2)
# # print(testing_tweets)

# # print(test_classify(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, testing_tweets))

# important_punctuation = '¯\\_(ツ)_/¯'


