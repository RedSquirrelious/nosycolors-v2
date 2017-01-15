from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
# from nltk.sentiment.util 

from gensim.summarization import summarize

import sys
import re
import string
import json
from collections import Counter

import enum
# from enum import enumerate


#reduce my typing
tokenizer = TweetTokenizer()

text_array = open('rose_test_raw.txt').read().split('\n')

punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '...', '…'] 

tf = Counter()

tweet = tokenizer.tokenize(text_array[0])

# print(tweet)


#summarization practice

with open('mlk_dream_speech.txt', 'r') as f:
    content = f.read()
    summary = summarize(content, split=True, word_count=100)
    for i, sentence in enumerate(summary):
        print("%d) %s" % (i+1, sentence))


# #processing tweets practice

def process(text, tokenizer=TweetTokenizer(), stopwords=[]):

	text = text.lower()
	tokens = tokenizer.tokenize(text)

	return [tok for tok in tokens if tok not in stopword_list and not tok.isdigit()]



# for tweet in text_array:
# 	tweet_tokenizer = TweetTokenizer()

# 	tokens = process(tweet, tokenizer=tweet_tokenizer, stopwords=stopword_list)

# 	tf.update(tokens)

# for tag, count in tf.most_common(20):
# 		print("{}: {}".format(tag, count))




import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
 
def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])
 
# evaluate_classifier(bigram_word_feats)
