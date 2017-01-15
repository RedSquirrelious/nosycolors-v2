from django.db import models


class EmotionManager(models.Manager):
	def create_emotion(self, emotion):
		new_emotion = self.create(emotion=emotion)

class Emotion(models.Model):
	emotion = models.CharField(max_length=20)
	objects = EmotionManager()

class WordManager(models.Model):
	def create_word(self, emotion):
		new_word = self.create(word=word)

class Word(models.Model):
	word = models.CharField(max_length=30)
	objects = WordManager()

