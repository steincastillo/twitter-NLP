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
Create a file named: auth.py

add the following lines:
consumer_key = 'your consumer key'
consumer_secret = 'your consumer secret'
access_token = 'your access token'
access_token_secret = 'your token secret'

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
import json
from pathlib import Path
import pandas as pd
from math import pi
import re
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer
from nltk.corpus import stopwords

#############
# Functions
#############

def read_json(json_file):
    with open(json_file) as file:
        list = json.load(file)
    return list

def pList(list):
    # Print a formated list of tuples
    for item in list:
        print (item[0], item[1], sep='-> ')

def pList1(list):
    # Print a formated list of tuples
    for item in list:
        print ('{:<20} {:^2} {:>20}'.format(item[0], '->', item[1]))

def load_badwords(lang):
    # Create the list of profanity words in different languages
    bad_words = []
    if lang == 'en':
        f = open ('bad_words_en.txt', 'r')
        bad_words = f.read()
        f.close()
        bad_words = nltk.word_tokenize(bad_words)
    elif lang == 'es':
        f = open ('bad_words_es.txt', 'r')
        bad_words = f.read()
        f.close()
        bad_words = nltk.word_tokenize(bad_words)
    return bad_words

def remove_links(text):
    urls = re.finditer('http\S+', text)
    for i in urls:
        try:
            text = re.sub(i.group().strip(), '', text)
        except:
            pass      
    return (text)

#############
# Constants
#############
# These constants control the behavior the this routine. Change them accordingly.
PRINT_OUT = False       # True if tweets should be display when processed
PUNCTUATION = [',', '.', '"', '“', '”', '!', '?', ':', '...', ';', "'", "’"]  # Punctuation symbols to eliminate
CLOUD_WORDS = 50        # Number of words to draw in the word cloud
READ_SPEED = 3      # 3 words per second

################
# Main Loop
################

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

# Validate the input file exists
file_check = Path(tweet_file)
if not(file_check.is_file()):
    # file does not exist
    print ('[Error] File does not exist.')
    exit()

# Define stopwords dictionary
if lang.lower() == 'es':
    stop_words = set(stopwords.words('spanish'))
    bad_words = load_badwords('es')
    print ('Using SPANISH stopwords list')
else:
    stop_words = set(stopwords.words('english'))
    bad_words = load_badwords('en')
    print ('Using ENGLISH stopwords list')

# Print routine header
print ('\n')
print('*'*(22+len(tweet_file)))
print('********** {} **********'.format(tweet_file.upper()))
print('*'*(22+len(tweet_file)))
print ('\n')

# Read the tweets file
print ('Reading tweets file...')
tweets = read_json(tweet_file)

# Extract and pre-process tweets text
print ('Extracting text from tweets...')
text = ''
for tweet in tweets:
    if tweet['truncated']:
        line = tweet['extended_tweet']['full_text']
    else:
        line = tweet['full_text']
    # Remove leading and trailing spaces
    line = line.strip()
    # Remove links
    line = remove_links(line)
    # Add line to text body
    text = text + line + '\n'

text_raw = text    

print ('Pre-processing the file...')

# Eliminate the punctuation signs
print ('Eliminating punctuation signs...')
for item in PUNCTUATION:
    text = text.replace(item, '')
# Eliminate new lines
print ('Eliminating new lines characters...')
text = text.replace('\n', ' ')
# Eliminate 'RT' flags
print ('Eliminating RT flags...')
text = text.replace('RT', '')
# Convert to lowercase
# print ('Converting to lowercase...')
# text.casefold()

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
used_stopwords = [word for word in tTokens if word in stop_words]

# Remove profanity
text_no_badwords = [word for word in tTokens if word.lower() not in bad_words]
used_bad_words = [word for word in tTokens if word.lower() in bad_words]

# Calculate frequency distribution
print ('Calculating frequency distribution...')
fdist = nltk.FreqDist(tTokens)
fdist1 = nltk.FreqDist(text_nonstop)
fdist2 = nltk.FreqDist(text_no_badwords)
fdist_stopwords = nltk.FreqDist(used_stopwords)
fdist_badwords = nltk.FreqDist(used_bad_words)
fdist_hash = nltk.FreqDist(tHash)    # Hash frequency distribution
fdist_at = nltk.FreqDist(tAt)       # @ frequcency distribution

# Create list with stopword count
used_stops = {}
for item in stop_words:
    if fdist[item]:
        used_stops[item]=fdist[item]

read_time = len(tTokens)/READ_SPEED/60

adj_vocab_rich = (len(text_vocab)-len(fdist_at)-len(fdist_stopwords)-len(fdist_badwords))/(len(tTokens))*100

# Display text file analysis
print ('\n****** Analysis Results *******')
print ('Sentences                   : {}'.format(len(sentence_tokens)))
print ('Total words                 : {}'.format(len(tTokens)))
print ('Unique words                : {}'.format(len(text_vocab)))
print ('Vocabulary richness         : {:.2f}%'.format(len(text_vocab)/len(tTokens)*100))
print ('Unique stopwords            : {}'.format(len(fdist_stopwords)))
print ('Total stopwords             : {}'.format(len(used_stopwords)))
print ('Unique profanity words      : {}'.format(len(fdist_badwords)))
print ('Total profanity words       : {}'.format(len(used_bad_words)))
print ('Adjusted vocabulary richness: {:.2f}'.format(adj_vocab_rich))
print ('Reading time                : {:.1f} min.'.format(read_time))
print ('*********************************')
print ('\n15 most common words:')
print ('-------------------------')
pList1(fdist.most_common(15))
print ('\n15 most common nonstop words:')
print ('-----------------------------------')
pList1(fdist1.most_common(15))
print ('\n15 most common stop words:')
print ('-----------------------------------')
pList1(fdist_stopwords.most_common(15))
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
