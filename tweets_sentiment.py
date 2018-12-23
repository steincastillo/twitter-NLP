#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
tweets_sentiment.py
Date created: 22-Nov-2018
Version: 1.0
Author: Stein Castillo
Copyright 2018 Stein Castillo <stein_castillo@yahoo.com>  

USAGE: python tweets_sentiment.py --file <tweets_file>
"""

#############
# Libraries
#############
import argparse
import warnings
from pathlib import Path
import pandas as pd
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize

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


#############
# Constants
#############
# These constants control the behavior the this routine. Change them accordingly.
PRINT_OUT = True       # True if tweets should be display when processed
FILE_DELIMITER = '|'    # CSV file delimiter
FILE_ENCODING = 'utf-8'


#construct the command line argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True,
    help='usage: python tweets_sentiment.py --file <file>')
args = vars(ap.parse_args())

warnings.filterwarnings("ignore")


# unpack command line arguments
tweet_file = args['file']

# Validate file exists
file_check = Path(tweet_file)
if not(file_check.is_file()):
    # file does not exist
    print ('[Error] File does not exist.')
    exit()

# Read the tweets file
print ('Reading tweets file...')
tweets = read_csv(tweet_file)

# Initialize NLTK sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Add features for sentiment analysis
tweets['textblob'] = 0.0
tweets['nltk'] = 0.0

# Analyze tweet sentiment
print ('Analyzing tweet sentiment...')

if PRINT_OUT:
    print('--------------------------------------------------------------------------------------------------------------')
    print ('TextBlob | NLTK |                          Tweet text                     | Sentences | Words  | Unique Words')
    print('--------------------------------------------------------------------------------------------------------------')

for index, item in tweets.iterrows():
    # Tokenize text
    tweet_sent = sent_tokenize(item[1])   # Tokenize sentences
    tweet_word = word_tokenize(item[1])   # Tokenize words
    tweet_unique = list(set(tweet_word))  # Eliminate duplicated words
    # Analyze setiment
    ss1 = TextBlob(item[1])
    ss2 = sid.polarity_scores(item[1])
    tweets['textblob'][index] = ss1.sentiment.polarity
    tweets['nltk'][index] = ss2['compound']
    # Display resutls
    if PRINT_OUT:
        print ('{:8.2f} | {:4.2f} | {:55.55} | {:9d} | {:6d} | {:12d}'.format(
                           ss1.sentiment.polarity, 
                           ss2['compound'],
                           item[1],
                           len(tweet_sent),
                           len(tweet_word),
                           len(tweet_unique)
                           ))

print ('\n-------------------------')
print ('Sentiment analysis summary:')
print ('TextBlob Average {:.2f}'.format(tweets['textblob'].mean()))
print ('NLTK Average {:.2f}'.format(tweets['nltk'].mean()))