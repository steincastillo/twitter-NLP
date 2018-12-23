# -*- coding: utf-8 -*-
"""
tweets_sentiment.py
Created on Thu Nov 22 20:45:46 2018
Version: 1.3
Author: Stein Castillo
Copyright 2018 Stein Castillo <stein_castillo@yahoo.com>

Summary:
************
This routine will plot (scatter) the sentinment analysis of a set of tweets.

Note that the maximum tweet count to download is 200 as this is limited by
the twitter API.

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
*************
python tweets_scatter.py --file <tweets_file>
"""

#############
# Libraries
#############
import pandas as pd
import numpy as np
import argparse
import warnings
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import style
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
PRINT_OUT = False       # True if tweets should be display when processed
FILE_DELIMITER = '|'    # CSV file delimiter
FILE_ENCODING = 'utf-8'

#############
# Main Loop
#############

#construct the command line argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True,
    help='usage: python tweets_scatter.py --file <file>')
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
    print ('TextBlob | NLTK | Tweet text')

total_records = len(tweets)-1

for index, item in tweets.iterrows():
    ss1 = TextBlob(item[1])
    ss2 = sid.polarity_scores(item[1])
    tweets['textblob'][index] = ss1.sentiment.polarity
    tweets['nltk'][index] = ss2['compound']
    if PRINT_OUT:
        print ('{:.2f} | {:.2f} | {}'.format(
                           ss1.sentiment.polarity, 
                           ss2['compound'],
                           item[1]))
    else:
        # display progress
        sys.stdout.write('\rAnalyzing record: ' + str(index) + ' of ' + str(total_records))
        sys.stdout.flush()  

print ('\nTweet analysis complete.')        
# Graph sentiment - scatter chart
print ('Creating chart...')
style.use('ggplot')

# Initialize figure
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

# Textblob Chart
ax1.scatter(tweets.index, tweets['textblob'],
            alpha=0.8, c='blue', edgecolors='none',
            s=30, label='Textblob', marker='H')

# Calculate trend line - Textblob
z1 = np.polyfit(tweets.index, tweets['textblob'], 1)
p1 = np.poly1d(z1)
ax1.plot(tweets.index, p1(tweets.index), '-.', color = 'blue')

# Add positive sentiment patch
ax1.add_patch(
        patches.Rectangle(
                (0,0),  # (x, y)
                total_records,  # Width
                1,  # height
                alpha = 0.3, facecolor='green'))
# Add negative sentiment patch
ax1.add_patch(
        patches.Rectangle(
                (0,0),  # (x, y)
                total_records,  # Width
                -1,  # height
                alpha = 0.3, facecolor='red'))
ax1.legend(loc=2)

# NLTK chart
ax2.scatter(tweets.index, tweets['nltk'],
             alpha=0.8, c='magenta', edgecolors='none',
             s=30, label='NLTK', marker='H')

# Calculate trend line - NLTK
z2 = np.polyfit(tweets.index, tweets['nltk'], 1)
p2 = np.poly1d(z2)
ax2.plot(tweets.index, p2(tweets.index), '-.', color = 'magenta')

# Add positive sentiment patch
ax2.add_patch(
        patches.Rectangle(
                (0,0),  # (x, y)
                total_records,  # Width
                1,  # height
                alpha = 0.3, facecolor='green'))
# Add negative sentiment patch
ax2.add_patch(
        patches.Rectangle(
                (0,0),  # (x, y)
                total_records,  # Width
                -1,  # height
                alpha = 0.3, facecolor='red'))
ax2.legend(loc=2)

# Add title
plt.suptitle('Sentiment Analysis-'+tweet_file)

# Show the chart
plt.show()