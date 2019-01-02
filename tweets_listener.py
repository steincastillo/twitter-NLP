#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tweets_listener.py
Date created: 30-Dec-2018
Version: 1.0
Author: Stein Castillo
Copyright 2018 Stein Castillo <stein_castillo@yahoo.com>  

Summary:
*********
This routine will listen to twitter live feed, collect the tweets and save
them to a CSV file that can be later be used to perform NLP analysis.

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
import csv
import pandas as pd

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

def save_to_csv(tweets, filename):
    # Create file
    with open(filename+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=FILE_DELIMITER)
        for item in tweets:
            writer.writerow(item)   
    csvfile.close()
    return

#############
# Constants
#############
# These constants control the behavior the this routine. Change them accordingly.
MAX_TWEETS = 300         # Number of tweets to download if not specified in command line
REMOVE_LINKS = True     # True if web links from message should be removed
PRINT_OUT = True       # True if tweets should be display when processed
FILE_DELIMITER = '|'    # CSV file delimiter

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
        self.maxcount = MAX_TWEETS 
        self.count = 1
        self.DELIMITER = '|'
        # Create file
        self.csvfile = open('listener.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csvfile, delimiter = self.DELIMITER)

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
                # Save tweets to cvs file
                print ('\n')
                print ('*****************')
                print ('Closing file...')
                self.csvfile.close()
                print ('File {} created. Process complete!'.format('listener'+'.csv'))
                return False
            
            # Process tweet information
            self.t_id = self.tweet['id']
            self.t_lang = self.tweet['lang']
            self.t_loc = self.tweet['user']['location']
            self.t_user = self.tweet['user']['screen_name']
    
            # Get tweet text
            if self.tweet['truncated']:
                self.t_full_text = self.tweet['extended_tweet']['full_text']
            else:
                self.t_full_text = self.tweet['text']

            # get in reply of tweet id
            if not(self.tweet['in_reply_to_status_id'] == None):
                self.t_in_reply_to = self.tweet['in_reply_to_status_id']
            else:
                self.t_in_reply_to =  'None'

            # Remove links from the tweet text    
            self.t_full_text = self.remove_links(self.t_full_text)

            # Remove leading and trailing spaces from message
            self.t_full_text = self.t_full_text.strip()

            # Create the line for the CSV file                        
            self.line = [self.t_id, self.t_full_text, self.t_lang, self.t_in_reply_to]

            # Write the line to the CSV file
            self.writer.writerow(self.line)
            self.csvfile.flush()

            # Print the message to STDOUT
            print ('{:4d} | @{} | {} | {}'.format(
            self.count,
            self.t_user,
            self.t_full_text,
            self.t_in_reply_to))
            
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
        help='usage: python tweets_sentiment.py --track <keyword> --lang <es|en>')
    ap.add_argument('-l', '--lang', default='en', required=False)
    args = vars(ap.parse_args())
    warnings.filterwarnings("ignore")

    # unpack command line arguments
    tweet_track = args['track']
    tweet_lang = args['lang'].lower()

    print ('\n')
    print ('***************************')
    print ('*    Twitter Listener     *')
    print ('***************************')

    print ('Listening to: {}'.format(tweet_track))
    print ('Language    : {}'.format(tweet_lang))
    print ('Getting     : {} tweets'.format(MAX_TWEETS))
    print ('***************************')
    print ('\n')

    stream = MyStreamer()

    stream.statuses.filter(track=tweet_track,
                        language=[tweet_lang], tweet_mode='extended')


