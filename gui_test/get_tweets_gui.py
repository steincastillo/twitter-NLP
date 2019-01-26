# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 16:51:58 2019

@author: stein
"""
#############
# Libraries
#############
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
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

qtCreatorFile = "get_tweets.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.getTweets.clicked.connect(self.fetchtweets)
       
    def fetchtweets(self):
        # Extract parameters
        tUser = self.user.text().lower()
        tCount = int(self.tweetCount.value())

        # Clear text windows
        self.statusDisplay.clear()
        self.tweetDisplay.clear()

        # Validate twitter user
        if self.user.text() == '':
            self.statusDisplay.append('[ERROR] User name cannot be blank!')
            return()
        try:
            user_details = twitter.lookup_user(screen_name=self.user.text())
        except:
            self.statusDisplay.append('[ERROR] User name not found in twitter!')
            return()

        # Validate user has enough tweets
        if user_details[0]['statuses_count'] < tCount:
            self.statusDisplay.append('[WARNING] User does not have enough tweets, Adjusting...')
            tCount = user_details[0]['statuses_count']
        
        self.statusDisplay.append('Downloading '+ str(tCount) + ' tweets of ' + user_details[0]['name'])

        # Display user details
        self.disId.setText(str(user_details[0]['id']))
        self.disName.setText(user_details[0]['name'])
        self.disCount.setText(str(user_details[0]['statuses_count']))
        self.disFollow.setText(str(user_details[0]['followers_count']))

        # Get user timeline
        try:
            user_timeline = twitter.get_user_timeline(screen_name = tUser,
                                                count = tCount,
                                                tweet_mode = 'extended')
            self.statusDisplay.append('Tweets succesfully retrieved!')
        except:
            self.statusDisplay.append('Tweets could not be retrived!')
            return()
        
        # Display retrieved tweets
        for tweet in user_timeline:
            line = '...{} | {}... '.format(
                tweet['id_str'][-4:],
                tweet['full_text'][0:100].replace('\n', ' '))
            self.tweetDisplay.append(line)

        # Save tweets to JSON file
        self.statusDisplay.append('Creating JSON file...')
        filename = tUser+'.json'

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(user_timeline, file, sort_keys = True, indent= 4)
        
        line = 'File {} created. Process complete!'.format(filename)
        self.statusDisplay.append(line)
      
if __name__ == "__main__":
    
    # Initialize tweeter port
    twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret)

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())