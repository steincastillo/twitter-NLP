# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 14:43:37 2019

@author: stein
"""

#############
# Libraries
#############
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import argparse
import warnings
import json
import re
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer

# Define UI
qtCreatorFile = "tweets_sentiment.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#############
# Classes
#############
class NormalizeText():   
    def remove_special(s):
        # Special characters dictionary
        SPECIAL_CHARS = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ü':'u',
                         'Á':'A', 'É':'E', 'Í':'I', 'Ó':'O', 'Ú':'U'}
        for char in SPECIAL_CHARS:
            s = s.replace(char, SPECIAL_CHARS[char])
        return s

    def to_lowercase(s):
        # Convert text to lowercase
        s = s.casefold()
        return s

    def remove_flags(s):
        # Flags dictionary
        FLAGS = {'RT':''}
        for flag in FLAGS:
            s = s.replace(flag, FLAGS[flag])
        return s

    def remove_nonascii(s):
        s = re.sub(r'[^\x00-\x7f]',r'', s)
        return s

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.fileName = ''
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.bSelectFile.clicked.connect(self.openFilenameDialog)
        self.bAnalyse.clicked.connect(self.tweetAnalyse)
        self.bClose.clicked.connect(self.closeEvent)
        self.tTweets.doubleClicked.connect(self.tDetails)
        
    def closeEvent(self):
        # Close the application
        app.quit()

    def tDetails(self):
        # Table double click, show the tweet text details
        # Get the location of the double click
        for idx in self.tTweets.selectionModel().selectedIndexes():
            row_number = idx.row()
            column_number = idx.column()
        # Get the text details
        item = self.tTweets.item(row_number, column_number)
        # Create a pop up window with the details
        QtWidgets.QMessageBox.about(self, 'Tweet', item.text())

    def read_json(self, json_file):
        with open(json_file) as file:
            list = json.load(file)
        file.close()
        return list

    def remove_links(self, text):
        urls = re.finditer('http\S+', text)
        for i in urls:
            try:
                text = re.sub(i.group().strip(), '', text)
            except:
                pass      
        return (text)

    def openFilenameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","JSON files (*.json)", options=options)
        if self.fileName:
            self.lFileName.setText(self.fileName)
            return
        else:
            return()

    def tweetAnalyse(self):
        # Read the tweets file
        if self.fileName == '':
            return
        self.lStatusline.setText('Reading JSON file...')
        tweets = self.read_json(self.fileName)

        # Initalize tweeter tokenizer
        tTokenizer = TweetTokenizer()

        # Initialize NLTK sentiment analyzer
        sid = SentimentIntensityAnalyzer()

        # Initialize cumulators for mean calculation
        tss1 = 0.0
        tss2 = 0.0
        tLine = 0

        # Initialize table
        self.tTweets.setRowCount(0)

        # Configure table
        # Disable table editing
        self.tTweets.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set column width
        self.tTweets.setColumnWidth(0, 60)      # Textblob
        self.tTweets.setColumnWidth(1, 60)      # NLTK
        self.tTweets.setColumnWidth(2, 345)     # Tweet text
        self.tTweets.setColumnWidth(3, 65)      # Sentences
        self.tTweets.setColumnWidth(4, 65)      # Words
        self.tTweets.setColumnWidth(5, 85)      # Unique words

        # Analyze tweet sentiment
        self.lStatusline.setText('Analyzing tweet sentiment...')
        for tweet in tweets:
            # get text from tweet
            if tweet['truncated']:
                line = tweet['extended_tweet']['full_text']
            elif 'text' in tweet:
                line = tweet['text']
            else:
                line = tweet['full_text']
                
            # Remove leading and trailing spaces
            line = line.strip()
            # Remove links
            line = self.remove_links(line)
            # Eliminate new lines
            line = line.replace('\n', ' ')
            # Remove non-ascii characters
            line = NormalizeText.remove_nonascii(line)
            # Remove special characters
            line = NormalizeText.remove_special(line)

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
            tweet.update({'sentiment':{'textblob':ss1.sentiment.polarity, 'nltk':ss2['compound']}})
           
            # Display results
            self.tTweets.insertRow(tLine)       # Insert a row in the table

            value = '{:.2f}'.format(ss1.sentiment.polarity)
            self.tTweets.setItem(tLine,0, QtWidgets.QTableWidgetItem(value))    # Textblob
            # Set cell color
            if ss1.sentiment.polarity > 0:
                self.tTweets.item(tLine, 0).setBackground(QtCore.Qt.green)
            elif ss1.sentiment.polarity < 0:
                self.tTweets.item(tLine, 0).setBackground(QtCore.Qt.red)
            
            value = '{:.2f}'.format(ss2['compound'])
            # Set cell color
            self.tTweets.setItem(tLine,1, QtWidgets.QTableWidgetItem(value))    # NLTK
            if ss2['compound'] > 0:
                self.tTweets.item(tLine, 1).setBackground(QtCore.Qt.green)
            elif ss2['compound'] < 0:
                self.tTweets.item(tLine, 1).setBackground(QtCore.Qt.red)

            value = '{:200.200}'.format(line)
            self.tTweets.setItem(tLine,2, QtWidgets.QTableWidgetItem(value))    # Tweet text
            value = '{:6d}'.format(len(tweet_sent))
            self.tTweets.setItem(tLine,3, QtWidgets.QTableWidgetItem(value))    # Sentences
            value = '{:6d}'.format(len(tweet_word))
            self.tTweets.setItem(tLine,4, QtWidgets.QTableWidgetItem(value))    # Words
            value = '{:6d}'.format(len(tweet_unique))
            self.tTweets.setItem(tLine,5, QtWidgets.QTableWidgetItem(value))    # Unique Words
            tLine += 1

        # Display sentiment averages
        value = '{:.2f}'.format(tss1/len(tweets))
        self.tblobAvg.setText(value)
        value = '{:.2f}'.format(tss2/len(tweets))
        self.nltkAvg.setText(value)

        # Update JSON file
        self.lStatusline.setText('Updating JSON file...')
        with open(self.fileName, 'w', encoding='utf-8') as file:
            json.dump(tweets, file, sort_keys=True, indent=4)
        file.close()

#############
# Main Loop
#############

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())