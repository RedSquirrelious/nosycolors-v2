from django.shortcuts import render, redirect

from django.urls import reverse

from django.http import HttpResponse, Http404, HttpResponseRedirect

from .models import Tweet, Target

from .forms import HandleForm

from django.conf import settings

# FOR LANGUAGE ANALYSIS
import string

## needed for identifying emotion with highest score
import operator
from operator import itemgetter



## needed for MySQL
import mysql.connector
from mysql.connector import MySQLConnection, Error, connect, errorcode

## NLTK, language analysis
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import *
## import nltk.classify.util, nltk.metrics
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords


punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '...', '…']


def index(request):


	return render(request, 'twittering/index.html')



def target(request):
	target_user_list = Target.objects.order_by('-target_name')[:5]
	context = {'target_user_list': target_user_list}
	return render(request, 'twittering/target.html', context)


def tweeting(request):

	if request.method == 'POST':
	    # create a form instance and populate it with data from the request:
		form = HandleForm(request.POST)

		if form.is_valid():

			target_handle = form.cleaned_data['target_handle']
			number_of_tweets = form.cleaned_data['number_of_tweets']
			
			rawtweepy = settings.AUTHORIZED_USER.user_timeline(screen_name=target_handle, count=number_of_tweets)

			tweets = list(map(lambda t:t.text, rawtweepy))

			context = {'target_handle': target_handle, 'tweets': tweets}

# if a GET (or any other method) we'll create a blank form
	else:
		form = HandleForm()


	
	return render(request, 'twittering/tweeting.html', context)


def detail(request, target_id):
	try:
		target = Target.objects.get(pk=target_id)
	except Target.DoesNotExist:
		raise Http404("No such target!")
	else:
		return render(request, 'twittering/detail.html', {'target': target}) 

# NEEDED FOR CLASSIFY
def process(text, tokenizer=TweetTokenizer(), stopwords=[]):

	text = text.lower()
	tokens = tokenizer.tokenize(text)

	return [tok for tok in tokens if tok not in stopword_list and not tok.isdigit()]

# NEEDED FRO CLASSIFY
def query_emolex(host, database, user, password, tweet_word):
	cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
	cursor = cnx.cursor(dictionary=True)


	query = ("SELECT w.word, e.emotion, w.count, wes.score, wes.word_id, wes.emotion_id, w.id, e.id FROM words w JOIN word_emotion_score wes ON wes.word_id = w.id JOIN emotions e ON e.id = wes.emotion_id WHERE w.word = '%s'" % tweet_word)

	cursor.execute(query)

	results = cursor.fetchall()

	emotion_list = []

	for emotion in results:
		average_score = emotion['score']/emotion['count']
		emotion_w_score = (emotion['emotion'], average_score)
		emotion_list.append(emotion_w_score)

	return emotion_list


	cursor.close()
	cnx.close()

# NEEDED FOR CLASSIFY

def find_strongest_emotion_for_word(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet_word):

	emotion_list = query_emolex(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, tweet_word)
	if not emotion_list:
		return []
	highest_scoring_emotion = max(emotion_list, key=itemgetter(1))[0]
	return highest_scoring_emotion

# NEEDED FOR CLASSIFY 

def find_strongest_emotions_in_tweet(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, word_list):
	emotion_list = []
	
	for word in word_list:
		highest_scoring_emotion = find_strongest_emotion_for_word(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, word)
		emotion_list.append(highest_scoring_emotion)
	
	return emotion_list




def classify(request):
	if request.method == 'POST':
	    # create a form instance and populate it with data from the request:
		form = HandleForm(request.POST)

		if form.is_valid():

			target_handle = form.cleaned_data['target_handle']
			number_of_tweets = form.cleaned_data['number_of_tweets']
			
			rawtweepy = settings.AUTHORIZED_USER.user_timeline(screen_name=target_handle, count=number_of_tweets)

			tweets = list(map(lambda t:t.text, rawtweepy))

			tester = tweets[0]

			tweet_words = process(tester)

			emotions_list = find_strongest_emotions_in_tweet(settings.HOST, settings.DATABASE_NAME, settings.USER_NAME, settings.DATABASE_KEY, tweet_words)



			context = {'target_handle': target_handle, 'tweets': tweets, 'emotions': emotions_list}
			# context = {'target_handle': target_handle, 'tweets': tweets}

# if a GET (or any other method) we'll create a blank form
	else:
		form = HandleForm()


	
	return render(request, 'twittering/classify.html', context)
