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

# Define UI
qtCreatorFile = "get_tweets.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        # Add status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        
        
        self.getTweets.clicked.connect(self.fetchtweets)
        self.bClose.clicked.connect(self.closeEvent)

    def closeEvent(self):
        # Close the application
        app.quit()
       
    def fetchtweets(self):
        # Get user tweets
        
        # Extract parameters
        tUser = self.user.text().lower()
        tCount = int(self.tweetCount.value())

        # Clear text windows
        self.statusDisplay.clear()
        self.tweetDisplay.clear()

        # Validate twitter user
        if self.user.text() == '':
            self.statusDisplay.append('<font style="color:Red;">[ERROR] User name cannot be blank!</font>')
            return()
        try:
            user_details = twitter.lookup_user(screen_name=self.user.text())
        except:
            self.statusDisplay.append('<font style="color:Red;">[ERROR] User name not found in twitter!</font>')
            return()

        # Validate user has enough tweets
        if user_details[0]['statuses_count'] < tCount:
            self.statusDisplay.append('<font style="color:Orange;">[WARNING] User does not have enough tweets, Adjusting...</font>')
            tCount = user_details[0]['statuses_count']
        
        self.statusDisplay.append('<font style="color:Green;">[MSG] Downloading '+ str(tCount) + ' tweets of ' + user_details[0]['name']+'</font>')

        # Display user details
        self.disId.setText(str(user_details[0]['id']))
        self.disName.setText(user_details[0]['name'])
        self.disCount.setText(str(user_details[0]['statuses_count']))
        self.disFollow.setText(str(user_details[0]['followers_count']))

        # Get user timeline
        self.statusBar.showMessage('Retrieving user tweets...', 1000)
        try:
            user_timeline = twitter.get_user_timeline(screen_name = tUser,
                                                count = tCount,
                                                tweet_mode = 'extended')
            self.statusDisplay.append('<font style="color:Green;">[MSG] Tweets succesfully retrieved!</font>')
        except:
            self.statusDisplay.append('<font style="color:Green;">[ERROR] Tweets could not be retrived!</font>')
            return()
        
        # Display retrieved tweets
        self.statusBar.showMessage('Displaying user tweets...', 1000)
        for tweet in user_timeline:
            line = '...{} | {}... '.format(
                tweet['id_str'][-4:],
                tweet['full_text'][0:100].replace('\n', ' '))
            self.tweetDisplay.append(line)

        # Save tweets to JSON file
        self.statusDisplay.append('<font style="color:Green;">[MSG] Creating JSON file.</font>')
        filename = tUser+'.json'

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(user_timeline, file, sort_keys = True, indent= 4)
        
        line = '<font style="color:Green;">[MSG] File {} created. Process complete!</font>'.format(filename)
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