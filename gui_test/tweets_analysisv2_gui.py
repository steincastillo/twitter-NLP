# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 12::34 2019

@author: stein
"""

import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer
from nltk.corpus import stopwords
from wordcloud import WordCloud, ImageColorGenerator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

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

    def remove_punctuation(s):
        # Remove punctuation marks
        # Punctuation symbols to eliminate
        PUNCTUATION = [',', '.', '"', '“', '”', '!', '¡', '?', '¿', ':', 
                       '...', ';', "'", "’", '…', '(', ')', '*', '-', '~']
        for item in PUNCTUATION:
            s = s.replace(item, '')
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

    def remove_links(s):
        urls = re.finditer('http\S+', s)
        for i in urls:
            try:
                s = re.sub(i.group().strip(), '', s)
            except:
                pass      
        return (s)

class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas, self)    #matplot lib toolbar. Not needed for wordcloud

        # Add interface elements
        
        # Header layout
        self.bSelectFile = QtWidgets.QPushButton('Select file...')
        self.lFileName = QtWidgets.QLineEdit()
        self.lFileName.setEnabled(False)

        self.l1 = QtWidgets.QLabel('Language:')
        self.cLang = QtWidgets.QComboBox()
        self.cLang.addItem('English')
        self.cLang.addItem('Spanish')

        self.bAnalyze = QtWidgets.QPushButton('Analyze')

        headerLayout = QtWidgets.QHBoxLayout()
        headerLayout.addWidget(self.bSelectFile)
        headerLayout.addWidget(self.lFileName)
        headerLayout.addWidget(self.l1)
        headerLayout.addWidget(self.cLang)
        headerLayout.addWidget(self.bAnalyze)


        # Bottom Layout
        self.tAnalysis = QtWidgets.QTextBrowser()
        self.tDetails = QtWidgets.QTextBrowser()

        bottomLayout = QtWidgets.QHBoxLayout()
        bottomLayout.addWidget(self.tAnalysis)
        bottomLayout.addWidget(self.tDetails)


        # Just some button connected to `plot` method
        # self.button = QtWidgets.QPushButton('Plot')
        # self.button.clicked.connect(self.plot)
        self.bSelectFile.clicked.connect(self.openFilenameDialog)
        self.bAnalyze.clicked.connect(self.tweetAnalyse)

        # set the layout
        layout = QtWidgets.QVBoxLayout()

        layout.addLayout(headerLayout)

        #layout.addWidget(self.toolbar) #matplot lib toolbar. Not needed for wordcloud
        layout.addWidget(self.canvas)
        # layout.addWidget(self.button)

        layout.addLayout(bottomLayout)

        
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # discards the old graph
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
    
    def openFilenameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","JSON files (*.json)", options=options)
        if self.fileName:
            self.lFileName.setText(self.fileName)
            return
        else:
            return()

    def read_json(self, json_file):
        with open(json_file) as file:
            list = json.load(file)
        file.close()
        return list

    def load_badwords(self, lang):
        # Create the list of profanity words in different languages
        bad_words = []
        if lang == 'en':
            f = open ('bad_words_en.txt', 'r')
            bad_words = f.read()
            f.close()
            bad_words = nltk.word_tokenize(bad_words)
        elif lang == 'es':
            f = open ('bad_words_es.txt', 'r')
            bad_words = f.read()
            f.close()
            bad_words = nltk.word_tokenize(bad_words)
        return bad_words

    def remove_links(self, text):
        urls = re.finditer('http\S+', text)
        for i in urls:
            try:
                text = re.sub(i.group().strip(), '', text)
            except:
                pass      
        return (text)

    def tweetAnalyse(self):

        # Clear text browser boxes
        self.tAnalysis.clear()
        self.tDetails.clear()

        # Read the tweets file
        if self.fileName == '':
            return
        # self.lStatusline.setText('Reading JSON file...')
        tweets = self.read_json(self.fileName)

        # Define stopwords dictionary
        # Read language combox selection
        lang = str(self.cLang.currentText()).lower()
        print (lang)
        if lang == 'spanish':
            stop_words = set(stopwords.words('spanish'))
            bad_words = self.load_badwords('es')
            print ('Using SPANISH stopwords/profanity dictionary')
        else:
            stop_words = set(stopwords.words('english'))
            bad_words = self.load_badwords('en')
            print ('Using ENGLISH stopwords/profanity dictionary')

        # Extract and pre-process tweets text
        # self.lStatusline.setText('Extracting text from tweets...')
        text = ''
        for tweet in tweets:
            if tweet['truncated']:
                line = tweet['extended_tweet']['full_text']
            elif 'text' in tweet:
                line = tweet['text']
            else:
                line = tweet['full_text']
            # Remove leading and trailing spaces
            line = line.strip()
            # Remove links
            line = NormalizeText.remove_links(line)
            # print (line)
            # Add line to text body
            text = text + line + '\n'

        # self.lStatusline.setText('Pre-processing file...')
        # Remove non-ascii characters
        # self.lStatusline.setText('Removing non-ascii characters...')
        text = NormalizeText.remove_nonascii(text)
        # Replace accent and special character
        # self.lStatusline.setText('Replacing special characters...')
        text = NormalizeText.remove_special(text)

        # Create a copy of the text
        text_raw = text

        # Eliminate the punctuation signs
        # self.lStatusline.setText('Eliminating punctuation signs...')
        text = NormalizeText.remove_punctuation(text)
        # Eliminate new lines
        # self.lStatusline.setText('Eliminating new lines characters...')
        text = text.replace('\n', ' ')
        # Eliminate 'RT' flags
        # self.lStatusline.setText('Eliminating RT flags...')
        text = NormalizeText.remove_flags(text)
        # Converting to lowercase
        # self.lStatusline.setText('Converting to lowercase...')
        text = NormalizeText.to_lowercase(text)

        # Tokenize words 
        # self.lStatusline.setText('Tokenizing tweets...')
        tTokenizer = TweetTokenizer()
        tTokens = tTokenizer.tokenize(text)
        # Tokenize sentences
        sentence_tokens = nltk.sent_tokenize(text_raw)

        # Extract @ and hashtags
        # self.lStatusline.setText('Analysing hashtags...')
        tHash = []
        tAt = []
        for item in tTokens:
            if re.search('^@.*', item):
                tAt.append(item)
            
            if re.search('^#.*', item):
                tHash.append(item)
                        
        # Create set with unique words
        text_vocab = set(tTokens)

        # Remove stop words
        text_nonstop = [word for word in tTokens if word not in stop_words]
        used_stopwords = [word for word in tTokens if word in stop_words]

        # Remove profanity
        text_no_badwords = [word for word in tTokens if word.lower() not in bad_words]
        used_bad_words = [word for word in tTokens if word.lower() in bad_words]

        # Calculate frequency distribution
        # self.lStatusline.setText('Calculating frequency distribution...')
        fdist = nltk.FreqDist(tTokens)
        fdist1 = nltk.FreqDist(text_nonstop)
        fdist2 = nltk.FreqDist(text_no_badwords)
        fdist_stopwords = nltk.FreqDist(used_stopwords)
        fdist_badwords = nltk.FreqDist(used_bad_words)
        fdist_hash = nltk.FreqDist(tHash)    # Hash frequency distribution
        fdist_at = nltk.FreqDist(tAt)       # @ frequcency distribution

        # Create list with stopword count
        used_stops = {}
        for item in stop_words:
            if fdist[item]:
                used_stops[item]=fdist[item]

        read_time = len(tTokens)/3/60

        adj_vocab_rich = (len(text_vocab)-len(fdist_at)-len(fdist_stopwords)-len(fdist_badwords))/(len(tTokens))*100

        # Display text file analysis results
        
        #line = 'Sentences                   : {}'.format(len(sentence_tokens))
        line = '{} {}'.format('Sentences:'.ljust(25, ' '), len(sentence_tokens))
        self.tAnalysis.append(line)
        # line = 'Total words                 : {}'.format(len(tTokens))
        line = '{} {}'.format('Total words:'.ljust(25, ' '), len(tTokens))
        self.tAnalysis.append(line)
        # line = 'Unique words                : {}'.format(len(text_vocab))
        line = '{} {}'.format('Unique words:'.ljust(25, ' '), len(text_vocab))
        self.tAnalysis.append(line)
        # line = 'Vocabulary richness         : {:.2f}%'.format(len(text_vocab)/len(tTokens)*100)
        line = '{} {:.2f}'.format('Vocabulary richness:'.ljust(25, ' '), len(text_vocab)/len(tTokens)*100)
        self.tAnalysis.append(line)
        #line = 'Unique stopwords            : {}'.format(len(fdist_stopwords))
        line = '{} {}'.format('Unique stopwords:'.ljust(25, ' '), len(fdist_stopwords))
        self.tAnalysis.append(line)
        #line = 'Unique profanity words      : {}'.format(len(fdist_badwords))
        line = '{} {:.0f}'.format('Unique profanity words:'.ljust(25, ' '), len(fdist_badwords))
        self.tAnalysis.append(line)
        #line = 'Total profanity words       : {}'.format(len(used_bad_words))
        line = '{} {:.0f}'.format('Total profanity words:'.ljust(25, ' '), len(used_bad_words))
        self.tAnalysis.append(line)
        #line = 'Adjusted vocabulary richness: {:.2f}'.format(adj_vocab_rich)
        line = '{} {:.2f}'.format('Adj. vocabulary richness:'.ljust(25, ' '), adj_vocab_rich)
        self.tAnalysis.append(line)
        #line = 'Reading time                : {:.1f} min.'.format(read_time)
        line = '{} {:.1f}'.format('Reading time:'.ljust(25, ' '), read_time)
        self.tAnalysis.append(line)

        
        # Plot the word cloud

        # discards the old graph
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # Generate word cloud
        wordcloud = WordCloud(stopwords=stop_words, max_words=50, background_color='white').generate(text)
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')

        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())