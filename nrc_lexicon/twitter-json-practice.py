import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import string

# NLTK, language analysis
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import *
# import nltk.classify.util, nltk.metrics
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords


tweets_data_path = 'ex-twitter-json.txt'

punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '...', '…']

tokenizer = TweetTokenizer()

def process(text, tokenizer=TweetTokenizer(), stopwords=[]):

	text = text.lower()
	tokens = tokenizer.tokenize(text)

	return [tok for tok in tokens if tok not in stopword_list and not tok.isdigit()]

def check_hashtag_position(word_array, word):
	if word_array[-1] or word_array[-2]  == word:
		print('it worked')


# GET TEST TEXT
tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

# print(len(tweets_data))

# tweet = tweets_data[0]

# text = tweet['text']

# print(text)

# clean_text = process(text)
# check_hashtag_position(clean_text, '#sadness')
# print(process(text))

# x = tweet.keys()

# print(x)




#CREATE DATAFRAME - !
tweets = pd.DataFrame()

# tweets['text'] = tweet['text']

#CREATE 3 COLUMNS IN DATAFRAME
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
# tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

# test = list(tweets['text'])

for tweet in tweets:
	for ch in map(tweet):
		print(ch)


# GET COUNT BY LANGUAGE
# print(tweets['lang'].value_counts()x[True])

# print(tweets_by_lang)

# fig, ax = plt.subplots()
# ax.tick_params(axis='x', labelsize=15)
# ax.tick_params(axis='y', labelsize=10)
# ax.set_xlabel('Languages', fontsize=15)
# ax.set_ylabel('Number of tweets' , fontsize=15)
# ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
# tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

#GET COUNT BY COUNTRY
# tweets_by_country = tweets['country'].value_counts()

# fig, ax = plt.subplots()
# ax.tick_params(axis='x', labelsize=15)
# ax.tick_params(axis='y', labelsize=10)
# ax.set_xlabel('Countries', fontsize=15)
# ax.set_ylabel('Number of tweets' , fontsize=15)
# ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
# tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')

#CHECK IF WORD IS PRESENT
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

# CLASSIFY TWEETS BY PRESENCE OF LANGUAGE IN TWEET
# tweets['python'] = tweets['text'].apply(lambda tweet: word_in_text('python', tweet))
# tweets['javascript'] = tweets['text'].apply(lambda tweet: word_in_text('javascript', tweet))
# tweets['ruby'] = tweets['text'].apply(lambda tweet: word_in_text('ruby', tweet))

# COUNT OF LANGUAGE NAME IN TWEET
# print tweets['python'].value_counts()[True]
# print tweets['javascript'].value_counts()[True]
# print tweets['ruby'].value_counts()[True]


#COMPARISON CHART
# prg_langs = ['python', 'javascript', 'ruby']
# tweets_by_prg_lang = [tweets['python'].value_counts()[True], tweets['javascript'].value_counts()[True], tweets['ruby'].value_counts()[True]]

# x_pos = list(range(len(prg_langs)))
# width = 0.8
# fig, ax = plt.subplots()
# plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')

# # Setting axis labels and ticks
# ax.set_ylabel('Number of tweets', fontsize=15)
# ax.set_title('Ranking: python vs. javascript vs. ruby (Raw data)', fontsize=10, fontweight='bold')
# ax.set_xticks([p + 0.4 * width for p in x_pos])
# ax.set_xticklabels(prg_langs)
# plt.grid()


# NARROW DOWN TWEET LIST BY DEFINING RELEVANT INFO, IN THIS CASE THE WORDS 'TUTORIAL' & 'PROGRAMMING'
# tweets['programming'] = tweets['text'].apply(lambda tweet: word_in_text('programming', tweet))
# tweets['tutorial'] = tweets['text'].apply(lambda tweet: word_in_text('tutorial', tweet))

# SPLIT THAT INTO ITS OWN COLUMN - RELEVANT TWEETS
# tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text('programming', tweet) or word_in_text('tutorial', tweet))


#GET COUNT OF RELEVANT TWEETS
# print tweets['programming'].value_counts()[True]
# print tweets['tutorial'].value_counts()[True]
# print tweets['relevant'].value_counts()[True]

# # COMPARE RELEVANT TWEETS AGAINST LANGUAGE TWEETS
# print tweets[tweets['relevant'] == True]['python'].value_counts()[True]
# print tweets[tweets['relevant'] == True]['javascript'].value_counts()[True]
# print tweets[tweets['relevant'] == True]['ruby'].value_counts()[True]


# # MAKE COMPARISON CHART BY LANGUAGE
# tweets_by_prg_lang = [tweets[tweets['relevant'] == True]['python'].value_counts()[True], 
#                       tweets[tweets['relevant'] == True]['javascript'].value_counts()[True], 
#                       tweets[tweets['relevant'] == True]['ruby'].value_counts()[True]]
# x_pos = list(range(len(prg_langs)))
# width = 0.8
# fig, ax = plt.subplots()
# plt.bar(x_pos, tweets_by_prg_lang, width,alpha=1,color='g')
# ax.set_ylabel('Number of tweets', fontsize=15)
# ax.set_title('Ranking: python vs. javascript vs. ruby (Relevant data)', fontsize=10, fontweight='bold')
# ax.set_xticks([p + 0.4 * width for p in x_pos])
# ax.set_xticklabels(prg_langs)
# plt.grid()

#EXTRACT LINKS FROM TWEETS
# def extract_link(text):
#     regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
#     match = re.search(regex, text)
#     if match:
#         return match.group()
#     return ''

# #ADD LINK COLUMN TO DATAFRAME
# tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))

# #PRINT RELEVANT TWEETS WITH LINK
# tweets_relevant = tweets[tweets['relevant'] == True]
# tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']