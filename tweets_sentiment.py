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
import json
import re
from pathlib import Path
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer

#############
# Functions
#############

def read_json(json_file):
    with open(json_file) as file:
        list = json.load(file)
    file.close()
    return list

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
PRINT_OUT = True       # True if tweets should be display when processed
UPDATE_FILE = True     # True if JSON file is updated with sentiment calculation
FILE_ENCODING = 'utf-8'

#############
# Main Loop
#############

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
tweets = read_json(tweet_file)

# Initalize tweeter tokenizer
tTokenizer = TweetTokenizer()

# Initialize NLTK sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Initialize cumulators for mean calculation
tss1 = 0.0
tss2 = 0.0

# Analyze tweet sentiment
print ('Analyzing tweet sentiment...')

if PRINT_OUT:
    print('--------------------------------------------------------------------------------------------------------------')
    print ('TextBlob | NLTK |                          Tweet text                     | Sentences | Words  | Unique Words')
    print('--------------------------------------------------------------------------------------------------------------')

for tweet in tweets:
    # get text from tweet
    if tweet['truncated']:
        line = tweet['extended_tweet']['full_text']
    else:
        line = tweet['full_text']
    # Remove leading and trailing spaces
    line = line.strip()
    # Remove links
    line = remove_links(line)

    # Tokenize text
    tweet_sent = sent_tokenize(line)   # Tokenize sentences
    tweet_word = tTokenizer.tokenize(line)
    tweet_unique = list(set(tweet_word))  # Eliminate duplicated words

    # Analyse sentiment
    ss1 = TextBlob(line)
    ss2 = sid.polarity_scores(line)

    # Update cumulators 
    tss1 += ss1.sentiment.polarity
    tss2 += ss2['compound']

    # Add sentiment results to the JSON
    if UPDATE_FILE:
        tweet.update({'sentiment':{'textblob':ss1.sentiment.polarity, 'nltk':ss2['compound']}})

    # Display results
    if PRINT_OUT:
        print ('{:8.2f} | {:4.2f} | {:55.55} | {:9d} | {:6d} | {:12d}'.format(
                           ss1.sentiment.polarity, 
                           ss2['compound'],
                           line,
                           len(tweet_sent),
                           len(tweet_word),
                           len(tweet_unique)
                           ))

print ('\n-------------------------')
print ('Sentiment analysis summary:')
print ('TextBlob Average {:.2f}'.format(tss1/len(tweets)))
print ('NLTK Average {:.2f}'.format(tss2/len(tweets)))

if UPDATE_FILE:
    # Update JSON file
    print ('\n')
    print ('*****************')
    print ('Updating JSON file...')
    with open(tweet_file, 'w', encoding='utf-8') as file:
        json.dump(tweets, file, sort_keys=True, indent=4)
    print ('File {} updated. Process complete!'.format(tweet_file))
    file.close()