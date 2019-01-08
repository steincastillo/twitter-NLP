# -*- coding: utf-8 -*-
"""
tweets_sentiment.py
Created on Thu Nov 22 20:45:46 2018
Version: 1.5
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
python tweets_scatter_v2.py --file <tweets_file>
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

#############
# Constants
#############
# These constants control the behavior the this routine. Change them accordingly.
PRINT_OUT = False       # True if tweets should be display when processed
UPDATE_FILE = True     # True if JSON file is updated with sentiment calculation

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
tweets = pd.read_json(tweet_file)

# Eliminate unnecesary features
# for feature in FEATURES:
#     tweets = tweets.drop(feature, axis=1)

# Validate sentiment analysis is done
if 'sentiment' not in tweets:
    print ('[Error] Execute sentiment analysis first...')
    exit()
       
# Graph sentiment - scatter chart

# Extract sentiment values
t_sentiment = tweets['sentiment'].apply(pd.Series)
total_records = len(tweets)-1
print ('Creating chart...')
style.use('ggplot')

# Initialize figure
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

# Textblob Chart
ax1.scatter(t_sentiment.index, t_sentiment['textblob'],
            alpha=0.8, c='blue', edgecolors='none',
            s=30, label='Textblob', marker='H')

# Calculate trend line - Textblob
z1 = np.polyfit(t_sentiment.index, t_sentiment['textblob'], 1)
p1 = np.poly1d(z1)
ax1.plot(t_sentiment.index, p1(t_sentiment.index), '-.', color = 'blue')

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
ax2.scatter(t_sentiment.index, t_sentiment['nltk'],
             alpha=0.8, c='magenta', edgecolors='none',
             s=30, label='NLTK', marker='H')

# Calculate trend line - NLTK
z2 = np.polyfit(t_sentiment.index, t_sentiment['nltk'], 1)
p2 = np.poly1d(z2)
ax2.plot(t_sentiment.index, p2(t_sentiment.index), '-.', color = 'magenta')

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