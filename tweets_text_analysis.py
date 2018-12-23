#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tweets_sentiment.py
Date created: 22-Dec-2018
Version: 1.5
Author: Stein Castillo
Copyright 2018 Stein Castillo <stein_castillo@yahoo.com>  

Summary:
*********
This routine will perform text analysis on a set of tweets. It will
produce an output that includes:
- Word count
- Sentence count
- Vocabulary richnness
- Number of stopwords used
- Estimated text reading time
- Most common words 
- Word cloud chart

Requisites:
***********
The input file MUST be produced with the routine tweets_get.py that is
part of this libary as the file format is very important.

The following libraries must be installed:
- NLTK
- Textblob
- WordCloud
- Matplotlib
- Pandas

USAGE: 
***********
python tweets_text_analysis.py --file <tweets_file> --lang <en|es>
"""

#############
# Libraries
#############
import argparse
import warnings
from pathlib import Path
import pandas as pd
import re
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer
from nltk.corpus import stopwords

#############
# Functions
#############
def read_csv(csv_file):
    # Read the tweet file
    pullData = pd.read_csv(csv_file, 
                               delimiter=FILE_DELIMITER,
                               header=None,
                               encoding=FILE_ENCODING,
                               na_filter = False)
    return (pullData)

def pList(list):
    # Print a formated list of tuples
    for item in list:
        print (item[0], item[1], sep='-> ')

def pList1(list):
    # Print a formated list of tuples
    for item in list:
        print ('{:<20} {:^2} {:>20}'.format(item[0], '->', item[1]))

#############
# Constants
#############
# These constants control the behavior the this routine. Change them accordingly.
PRINT_OUT = True       # True if tweets should be display when processed
FILE_DELIMITER = '|'    # CSV file delimiter
FILE_ENCODING = 'utf-8'
PUNCTUATION = [',', '.', '"', '“', '”', '!', '?', ':', '...', ';']  # Punctiation symbols to eliminate
CLOUD_WORDS = 50        # Number of words to draw in the word cloud
READ_SPEED = 3      # 3 words per second

################
# Main Loop
###############

#construct the command line argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True,
    help='usage: python tweets_sentiment.py --file <file> --lang <es|en>')
ap.add_argument('-l', '--lang', default='en', required=False)
args = vars(ap.parse_args())

warnings.filterwarnings("ignore")

# unpack command line arguments
tweet_file = args['file']
lang = args['lang']

# Define stopwords dictionary
if lang.lower() == 'es':
    stop_words = set(stopwords.words('spanish'))
    print ('Using SPANISH stopwords list')
else:
    stop_words = set(stopwords.words('english'))
    print ('Using ENGLISH stopwords list')

# Validate the input file exists
file_check = Path(tweet_file)
if not(file_check.is_file()):
    # file does not exist
    print ('[Error] File does not exist.')
    exit()

print ('\n')
print('*'*(22+len(tweet_file)))
print('********** {} **********'.format(tweet_file.upper()))
print('*'*(22+len(tweet_file)))
print ('\n')

# Read the tweets file
print ('Reading tweets file...')
tweets = read_csv(tweet_file)

# Extract tweets text
print ('Extracting text from tweets...')
text = ''
for index, line in tweets.iterrows():
    text = text + '\n' + line[1]

text_raw = text    

print ('Pre-processing the file...')

# Eliminate the punctuation signs
print ('Eliminating punctuation signs...')
for item in PUNCTUATION:
    text = text.replace(item, '')
# Eliminate new lines
print ('Eliminating new lines characters...')
text = text.replace('\n', ' ')
# Convert to lowercase
print ('Converting to lowercase...')
text.casefold()

# Tokenize words 
print ('Tokenizing tweets...')
tTokenizer = TweetTokenizer()
tTokens = tTokenizer.tokenize(text)
# Tokenize sentences
sentence_tokens = nltk.sent_tokenize(text_raw)

# Extract @ and hashtags
print ('Analysing hashtags...')
tHash = []
tAt = []
for item in tTokens:
    if re.search('^@.*', item):
       tAt.append(item)
    
    if re.search('^#.*', item):
       tHash.append(item)
                 
# Create set with unique words
text_vocab = set(tTokens)

# Remove stop words
text_nonstop = [word for word in tTokens if word not in stop_words]

# Calculate frequency distribution
print ('Calculating frequency distribution...')
fdist = nltk.FreqDist(tTokens)
fdist1 = nltk.FreqDist(text_nonstop)
fdist_hash = nltk.FreqDist(tHash)    # Hash frequency distribution
fdist_at = nltk.FreqDist(tAt)       # @ frequcency distribution

# Create list with stopword count
used_stops = {}
for item in stop_words:
    if fdist[item]:
        used_stops[item]=fdist[item]

read_time = len(tTokens)/READ_SPEED/60

# Display text file analysis
print ('\n****** Analysis Results *******')
print ('Sentences: {}'.format(len(sentence_tokens)))
print ('Words: {}'.format(len(tTokens)))
print ('Unique words: {}'.format(len(text_vocab)))
print ('Vocabulary richness: {:.2f}%'.format(len(text_vocab)/len(tTokens)*100))
print ('Number of stopwords: {}'.format(len(tTokens)-len(text_nonstop)))
print ('Reading time: {:.1f} min.'.format(read_time))
print ('\nTop 15 more common words:')
print ('-------------------------')
pList1(fdist.most_common(15))
print ('\nTop 15 more common nonstop words:')
print ('-----------------------------------')
pList1(fdist1.most_common(15))
print ("\nMost common #'s:")
print ('------------------')
pList1(fdist_hash.most_common(5))
print ("\nMost common @'s:")
print ('------------------')
pList1(fdist_at.most_common(15))

# Generate word cloud
wordcloud = WordCloud(stopwords=stop_words, max_words=CLOUD_WORDS, background_color='white').generate(text)
# Display the word cloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
