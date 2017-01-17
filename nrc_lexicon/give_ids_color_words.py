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


# ********LEXICON DATABASE ACCESS***********

with open(os.path.dirname(__file__) + '../.env') as secrets:

	lies = dict(ast.literal_eval(secrets.read()))
	USER_NAME = lies['USER_NAME']
	DATABASE_NAME = lies['DATABASE_NAME']
	DATABASE_KEY = lies['DATABASE_KEY']
	HOST = lies['HOST']

# *******************


def query_emolex(host, database, user, password, desired_word):
	cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
	cursor = cnx.cursor(dictionary=True)

	query = ("SELECT id, word FROM color_words WHERE word = '%s'" % desired_word)

	cursor.execute(query)

	results = cursor.fetchall()
	# print(results)

	for word in results:
	# 	# the_id = word['id'].format('id')
	# 	# the_word = word['word'].format('word')
	# 	print('meh')
		return word['id'], word['word']

	cursor.close()
	cnx.close()

with open('words_wo_id_colorid_votes.txt') as f:
# with open('color_lexicon_words_no_ids.txt') as f:
	text = f.read().strip().split('\n')

	words_wo_id = []
	for test_word in text:
		words = test_word.split()
		# print(words)
		the_word = words[0]
		color_id_votes = words[1:]

		x = query_emolex(HOST, DATABASE_NAME, USER_NAME, DATABASE_KEY, the_word)

		if not x:
			words_wo_id.append(test_word)
			# print('nope')
		else:
			y = x + (color_id_votes,)
			print(y)

