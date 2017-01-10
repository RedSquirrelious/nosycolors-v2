# testit.py

import tweepy
from tweepy import OAuthHandler

import ast


with open('.env') as secrets:
	lies = dict(ast.literal_eval(secrets.read()))

	CONSUMER_KEY = lies['CONSUMER_KEY']
	CONSUMER_SECRET = lies['CONSUMER_SECRET']
	ACCESS_SECRET = lies['ACCESS_SECRET']
	ACCESS_TOKEN = lies['ACCESS_TOKEN']
	CALLBACK_URL = lies['CALLBACK_URL']

# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)





api = tweepy.API(auth)

user = api.me()

print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friend Count: ' + str(user.friends_count))
print('Follower Count: ' + str(user.followers_count))


for status in tweepy.Cursor(api.user_timeline).items(2):
	print(status.text)

target = ''

# thing = api.user_timeline(screen_name=target, count=70, include_rts=False)

thing = api.user_timeline(screen_name=target, count=70)

# print(thing.text)

for tweet in thing:

	# if not tweet.text.startswith('RT'):
	# 	print(str(tweet.retweet_count))
		# print(tweet.text)
	# else:
	# 	print('you lose')
# Create your models here.
