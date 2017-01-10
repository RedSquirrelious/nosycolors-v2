from django.db import models

from django.utils import timezone

import datetime
# Create your models here.

#OAUTH TRACKING
# class NosyPerson(models.Model):
# 	nosyperson = API.get_user(screen_name)
# 	nosyperson_name = nosyperson.name
# 	nosyperson_handle = screen_name


class TargetManager(models.Manager):
	def create_target(self, target_handle, api):
		twitter_target = api.get_user(screen_name = target_handle)

		new_target = self.create(target_name=twitter_target.name, target_handle=twitter_target.screen_name, target_twitter_id=twitter_target.id)



class Target(models.Model):
	target_name = models.CharField(max_length=100)
	target_handle = models.CharField(max_length=15)
	target_twitter_id = models.BigIntegerField() 

	objects = TargetManager()

	def __str__(self):
		return self.target_name

	def what_handle(self):
		return self.target_handle



class TweetManager(models.Manager):
	def get_target_tweets(self, target_handle, api):
		tweet_list = api.user_timeline(screen_name=target_handle, count=100, includes_rts=False)

		for tweet in tweet_list:
			new_tweet = self.create(tweet_text=tweet.text, tweet_date=tweet.created_at, tweet_id=tweet.id, tweet_user_tw_id=tweet.user.id, tweet_user_handle=tweet.user.screen_name)



class Tweet(models.Model):

	tweet_text = models.CharField(max_length = 140)
	tweet_date = models.DateTimeField('date tweeted')
	target_user = models.ForeignKey(Target)
	tweet_id = models.BigIntegerField()
	tweet_user_tw_id = models.BigIntegerField()
	tweet_user_handle = models.CharField(max_length=15)

	objects = TweetManager()

	def __str__(self):
		return self.tweet_text

	def was_tweeted_in_last_7_days(self):
		return self.tweet_date >= timezone.now() - datetime.timedelta(days = 7)

