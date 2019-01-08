#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
get_tweets.py
Date created: 10-Nov-2018
Version: 2.0
Author: Stein Castillo
Copyright 2018 Stein Castillo <stein_castillo@yahoo.com>  

Summary:
************
This routine will fetch the tweets of an specific user and create a JSON file
with the results. This file can be used with the analysis tools of this libary:
    * tweets_sentiment.py : Analyze tweets sentiment
    * tweets_text_analisys.py: Text analysis
    * tweets_scatter_v2.py: Plot sentiment analysis

Note that the maximum tweet count to download is 200 as this is limited by
the twitter API.

Requisites:
***********
The following libraries must be installed:
- NLTK
- WordCloud
- Matplotlib
- Pandas

USAGE: 
***********
python tweets_get.py --user <twitter_user> [--count <number_of_tweets>]

note: the maximum number of tweets is 200
"""

#############
# Libraries
#############
from twython import Twython
import re
import json
import argparse
import warnings

# Get Twitter authentication credentials
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)

#############
# Functions
#############
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
MIN_TWEETS = 10         # Number of tweets to download in not specified in command line
PRINT_OUT = False        # Display retrieved tweets?

#############
# Main Loop
#############

print ('\n')
print ('***************************')
print ('*    Twitter Download     *')
print ('***************************')
print ('\n')

#construct the command line argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-u', '--user', required=True,
    help='usage: python tweets_get.py --user <user> --count <tweet_count>')
ap.add_argument('-c', '--count', required=False)
args = vars(ap.parse_args())
warnings.filterwarnings("ignore")

# unpack command line arguments
user = args["user"].lower()
count = args['count']

# Validate number of tweets to get
if count == None: 
    count = MIN_TWEETS
elif not (count.isdigit()): 
    count = MIN_TWEETS
count = int(count)

# Initialize tweeter port
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)

# Validate user name
user_details = []
try:
    user_details = twitter.lookup_user(screen_name=user)
except:
    print ('[ERROR] User name not found in twitter!')
    exit()

if len(user_details) == 0:
    print ('[ERROR] User name not found in twitter!')
    exit(0)

# Validate user has enough tweets to download
if count > 200:
    print ('[WARNING] Tweet count cannot be greater that 200. Adjusting...')
    count = 200
if user_details[0]['statuses_count'] < count:
    print ('[WARNING] User does not have enough tweets, Adjusting...')
    count = user_details[0]['statuses_count']

print ('Downloading {} tweet(s) of:'.format(count))    
print ('id: {} | name: {} | screen name: {} | Tweets: {} | Followers: {}'.format(
        user_details[0]['id'],
        user_details[0]['name'],
        user_details[0]['screen_name'],
        user_details[0]['statuses_count'],
        user_details[0]['followers_count']))
print ('\n')

# Get user timeline
try:
    user_timeline = twitter.get_user_timeline(screen_name = user,
                                          count = count,
                                          tweet_mode = 'extended')
    print ('Tweets succesfully retrieved!')
except:
    raise ValueError('Tweets could not be retrived!')

# Display retrieved tweets
if PRINT_OUT:
    print ('\n')
    for tweet in user_timeline:
        print ('...{} | {}... |'.format(
            tweet['id_str'][-4:],
            tweet['full_text'][0:90].replace('\n', ' ')
        ))
    print ('\n')

# Save tweets to JSON file
print ('Creating JSON file...')
filename = user+'.json'

with open(filename, 'w', encoding='utf-8') as file:
    json.dump(user_timeline, file, sort_keys = True, indent= 4)

print ('File {} created. Process complete!'.format(filename))
