import scattertext as ST
import tarfile, urllib, io
import pandas as pd

data = open('mlk_dream_speech.txt').read().strip()

quote = data[0:988]

test = quote.split('.')

quote_list = list(map(lambda t:t.strip() + '.', test))



print(quote_list[:3])