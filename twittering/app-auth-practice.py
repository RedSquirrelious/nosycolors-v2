import os
import ast
import tweepy
import jsonpickle

from tweepy import AppAuthHandler

from django.shortcuts import render, redirect

from django.urls import reverse

from django.http import HttpResponse, Http404, HttpResponseRedirect



from django.conf import settings


search_query = '#shock' #hashtag of interest
max_tweets = 10000 #some arbitrary large number
tweets_per_query = 100 #max Twitter API permits
file_name = 'shock_tweets.txt' #where I'll store these tweets
# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
since_id = 0
max_id = 0

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

# *************************************
# NOT SURE IF THIS BELONGS HERE??
# TWITTER_AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# TWITTER_AUTH.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# has a greater rate limit than OAuth
TWITTER_AUTH = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)


api = tweepy.API(TWITTER_AUTH, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if not api:
	print("can't authenticate")
	sys.exit(-1)

tweet_count = 0
print("Downloading max {0} tweets".format(max_tweets))
with open(file_name, 'w') as f:
    while tweet_count < max_tweets:
        try:
            if (max_id <= 0):
                if (not since_id):
                    new_tweets = api.search(q=search_query, count=tweets_per_query)
                else:
                    new_tweets = api.search(q=search_query, count=tweets_per_query,
                                            since_id=since_id)
            else:
                if (not since_id):
                    new_tweets = api.search(q=search_query, count=tweets_per_query,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=search_query, count=tweets_per_query,
                                            max_id=str(max_id - 1),
                                            since_id=since_id)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweet_count += len(new_tweets)
            print("Downloaded {0} tweets".format(tweet_count))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweet_count, file_name))
