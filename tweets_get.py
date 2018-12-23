#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
get_tweets.py
Date created: 10-Nov-2018
Version: 1.7
Author: Stein Castillo
Copyright 2018 Stein Castillo <stein_castillo@yahoo.com>  

Summary:
************
This routine will fetch the tweets of an specific user and create a CSV file
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
import csv
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
MIN_TWEETS = 10         # Number of tweets to download in not specified in command line
REMOVE_LINKS = True     # True if web links from message should be removed
PRINT_OUT = False       # True if tweets should be display when processed
FILE_DELIMITER = '|'    # CSV file delimiter

#############
# Main Loop
#############

#construct the command line argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-u', '--user', required=True,
    help='usage: python tweets_get.py --user <user> --count <tweet_count>')
ap.add_argument('-c', '--count', required=False)
args = vars(ap.parse_args())
warnings.filterwarnings("ignore")

# unpack command line arguments
user = args["user"]
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
    raise ValueError ('user name not found in twitter!')

if len(user_details) == 0:
    print ('User name not found in twitter!')
    exit(0)

# Validate user has enough tweets to download
if count > 200:
    print ('tweet count cannot be greater that 200. Adjusting')
    count = 200
if user_details[0]['statuses_count'] < count:
    print ('User does not have enough tweets, Adjusting...')
    count = user_details[0]['statuses_count']

# Print details of tweets to get
print ('Downloading {} tweet(s) of:'.format(count))    
print ('id: {} | name: {} | screen name: {} | Tweets: {}'.format(
        user_details[0]['id'],
        user_details[0]['name'],
        user_details[0]['screen_name'],
        user_details[0]['statuses_count']))

# Get user timeline
try:
    user_timeline = twitter.get_user_timeline(screen_name = user,
                                          count = count,
                                          tweet_mode = 'extended')
    print ('Tweets succesfully retrieved!')
except:
    raise ValueError('Tweets could not be retrived!')

# Pre-proccess tweets
print('Pre-processing tweets...')

if PRINT_OUT:
    print('ID | Full text | Lang')
 
tweet_list = []
    
for tweet in user_timeline:
    # Get tweet ID
    t_id = tweet['id']
    t_lang = tweet['lang']
    
    # Get tweet text
    if tweet['retweeted']:
        t_full_text = tweet['retweeted_status']['full_text']
    else:
        t_full_text = tweet['full_text']
    
    # Remove links from the tweet text    
    if REMOVE_LINKS:
        t_full_text = remove_regex(t_full_text, 'http\S+')
        
    # Remove leading and trailing spaces from message
    t_full_text = t_full_text.strip()
        
    # get in reply of tweet id
    if not(tweet['in_reply_to_status_id'] == None):
        t_in_reply_to = tweet['in_reply_to_status_id']
    else:
        t_in_reply_to =  'None'
    
    # Create the line for the CSV file                        
    line = [t_id, t_full_text, t_lang, t_in_reply_to]
    tweet_list.append(line)
        
    if PRINT_OUT:
        print ('...{} | {} | {} | {}'.format(
                str(t_id)[-4:],
                t_full_text,
                t_lang,
                t_in_reply_to))

print ('Pre-processing complete!')

# Save tweets to cvs file
print ('Creating csv file...')
save_to_csv(tweet_list, user)
print ('File {} created. Process complete!'.format(user+'.csv'))