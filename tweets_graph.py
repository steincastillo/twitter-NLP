# -*- coding: utf-8 -*-
"""
tweets_sentiment.py
Created on Thu Jan 13 21:33:47 2019
Version: 1.5
Author: Stein Castillo
Copyright 2018 Stein Castillo <stein_castillo@yahoo.com>

Summary:
************
This routine will plot (scatter) the sentinment analysis of a set of tweets
and the user tweeting frequency (line).

Requisites:
***********
The input file MUST be produced with the routine tweets_get.py that is
part of this libary as the file format is very important.

Prior to graphing the results the tweets_sentiment.py must be executed
on the file to calculate the tweets sentiment.

The following libraries must be installed:
- Matplotlib
- Pandas

USAGE:
*************
python tweets_graph.py --file <tweets_file.json>
"""

#############
# Libraries
#############
import pandas as pd
import numpy as np
import argparse
import warnings
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import style

#############
# Main Loop
#############

#construct the command line argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True,
    help='usage: python tweets_graph.py --file <file>')
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

# Validate sentiment analysis is done
if 'sentiment' not in tweets:
    print ('[Error] Execute sentiment analysis first...')
    exit()

# Extract sentiment values
print ('Extracting tweet sentiment values..')
t_sentiment = tweets['sentiment'].apply(pd.Series)
total_records = len(tweets)-1

# Extract tweeting frequency
print ('Calculating tweeting frequency...')
t_dates = tweets['created_at'].apply(pd.Series)
t_dates = t_dates.rename(columns={0:'date'})

# Extract dates and count frequency
d1 = []
for index, d in t_dates.iterrows():
    d1.append(d['date'].date())
    
t1 = pd.DataFrame({'date':d1})
f1=t1['date'].value_counts()

# Create chart
print ('Creating chart...')
style.use('ggplot')

# Initialize figure
fig, axes = plt.subplots(nrows=2, ncols=1)

# Tweet frequency chart
f1.plot(ax=axes[0])
axes[0].set_title('Tweet frequency-'+tweet_file)
axes[0].set_ylabel('# of tweets')

# NLTK sentiment chart
axes[1].scatter(t_sentiment.index, t_sentiment['nltk'],
             alpha=0.8, c='magenta', edgecolors='none',
             s=30, label='NLTK', marker='H')

axes[1].set_ylabel('Sentiment')
axes[1].set_title('Sentiment Analysis')

# Calculate trend line - NLTK
z2 = np.polyfit(t_sentiment.index, t_sentiment['nltk'], 1)
p2 = np.poly1d(z2)
axes[1].plot(t_sentiment.index, p2(t_sentiment.index), '-.', color = 'magenta')

# Add positive sentiment patch
axes[1].add_patch(
        patches.Rectangle(
                (0,0),  # (x, y)
                total_records,  # Width
                1,  # height
                alpha = 0.3, facecolor='green'))
# Add negative sentiment patch
axes[1].add_patch(
        patches.Rectangle(
                (0,0),  # (x, y)
                total_records,  # Width
                -1,  # height
                alpha = 0.3, facecolor='red'))
axes[1].legend(loc=2)

# Show the chart
plt.show()