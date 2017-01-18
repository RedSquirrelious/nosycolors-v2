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
from nltk.stem import WordNetLemmatizer

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


example_sent = "This is a sample sentence, showing off the stop words filtration."

stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(example_sent)

filtered_sentence = [w for w in word_tokens if not w in stop_words]

filtered_sentence = []

for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

# print(word_tokens)
# print(filtered_sentence)


ps = PorterStemmer()

example_words = ["python","pythoner","pythoning","pythoned","pythonly"]
more_example_words = ['rich', 'richer', 'richly', 'richest']

# for w in more_example_words:
#     print(ps.stem(w))

new_text = "It is important to by very pythonly while you are pythoning with python. All pythoners have pythoned poorly at least once."

words = word_tokenize(new_text)

# for w in words:
#     print(ps.stem(w))


wnl = WordNetLemmatizer()

for w in more_example_words:
	print(wnl.lemmatize(w))