#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tweets_listener.py
Date created: 30-Dec-2018
Version: 1.5
Author: Stein Castillo
Copyright 2018 Stein Castillo <stein_castillo@yahoo.com>  

Summary:
*********
This routine will listen to twitter live feed, collect the tweets and save
them to a JSON file that can be later be used to perform NLP analysis.

It will take two parameters:
Track: (Mandatory) that determines the key word to listen to
Lang: (Optional) sets the language to listen to. if not provided English will be used as default

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
python tweets_listener.py --track <keyword> --lang <en|es>
"""

#############
# Libraries
#############
from twython import Twython
from twython import TwythonStreamer
from textblob import TextBlob
import argparse
import warnings
import re
import json

# Get Twitter authentication credentials
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)

# Functions
def remove_regex(input_text, regex_pattern):
    # Remove a regular expression (regex) from a string
    urls = re.finditer(regex_pattern, input_text)
    for i in urls:
        try:
            input_text = re.sub(i.group().strip(), '', input_text)
        except:
            print ('Regex exception')

    return input_text

#############
# Constants
#############
# These constants control the behavior the this routine. Change them accordingly.
DEFAULT_TWEETS = 10     # Number of tweets to download if value is invalid or not provided
REMOVE_LINKS = True     # True if web links from message should be removed
PRINT_OUT = True       # True if tweets should be display when processed

#############
# Classes
#############

# Listening to tweets
class MyStreamer(TwythonStreamer):

    def __init__(self):
        TwythonStreamer.__init__(self,consumer_key,
                                    consumer_secret,
                                    access_token,
                                    access_token_secret)
        self.tweet_list = []
        self.maxcount = max_tweets 
        self.count = 1

    def remove_links(self, text):
        self._input_text = text
        self.urls = re.finditer('http\S+', self._input_text)
        for self.i in self.urls:
            try:
                self._input_text = re.sub(self.i.group().strip(), '', self._input_text)
            except:
                pass      
        return (self._input_text)
    
    def on_success(self, msg):
        self.tweet = msg
        if 'text' in self.tweet:
            
            if self.count > self.maxcount:
                self.disconnect()
                # Save tweets to JSON file
                print ('\n')
                print ('*****************')
                print ('Creating JSON file...')
                with open('listener.json', 'w', encoding='utf-8') as file:
                    json.dump(self.tweet_list, file, sort_keys=True, indent=4)
                print ('File {} created. Process complete!'.format('listener'+'.json'))
                return False
            
            self.tweet_list.append(self.tweet)

            # Print the message to STDOUT
            print ('{:4d} | ...{} | @{} | {}'.format(
            self.count,
            self.tweet['id_str'][-4:],
            self.tweet['user']['screen_name'],
            self.tweet['text'][0:90].replace('\n', ' ')))
            
            # Update the message counter
            self.count += 1

    def on_error(self, status_code, data):
        print (status_code)
        self.disconnect()

#############
# Main Loop
#############        

if __name__ == "__main__":

    #construct the command line argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--track', required=True,
        help='usage: python tweets_sentiment.py --track <keyword> [--count <count>] [--lang <es|en>]')
    ap.add_argument('-c', '--count', default = '10', required=False)
        help='usage: python tweets_listener.py --track <keyword> --lang <es|en>')
    ap.add_argument('-l', '--lang', default='en', required=False)
    
    args = vars(ap.parse_args())
    warnings.filterwarnings("ignore")

    # unpack command line arguments
    tweet_track = args['track']
    tweet_lang = args['lang'].lower()
    tweet_count = args['count']

    if tweet_count.isdigit():
        max_tweets = int(tweet_count)
    else:
        max_tweets = DEFAULT_TWEETS

    print ('\n')
    print ('***************************')
    print ('*    Twitter Listener     *')
    print ('***************************')

    print ('Listening to: {}'.format(tweet_track))
    print ('Language    : {}'.format(tweet_lang))
    print ('Getting     : {} tweets'.format(max_tweets))
    print ('***************************')
    print ('\n')

    stream = MyStreamer()

    stream.statuses.filter(track=tweet_track,
                        language=[tweet_lang], tweet_mode='extended')


