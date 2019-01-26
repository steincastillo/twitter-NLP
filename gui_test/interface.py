# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_tweets.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_get_tweets(object):
    def setupUi(self, get_tweets):
        get_tweets.setObjectName("get_tweets")
        get_tweets.resize(810, 483)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        get_tweets.setFont(font)
        self.centralwidget = QtWidgets.QWidget(get_tweets)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 10, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tweetDisplay = QtWidgets.QTextBrowser(self.centralwidget)
        self.tweetDisplay.setGeometry(QtCore.QRect(30, 100, 751, 221))
        self.tweetDisplay.setObjectName("tweetDisplay")
        self.statusDisplay = QtWidgets.QTextBrowser(self.centralwidget)
        self.statusDisplay.setGeometry(QtCore.QRect(30, 350, 751, 81))
        self.statusDisplay.setObjectName("statusDisplay")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 50, 431, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.user = QtWidgets.QLineEdit(self.widget)
        self.user.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.user.setMaxLength(24)
        self.user.setObjectName("user")
        self.horizontalLayout.addWidget(self.user)
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.tweetCount = QtWidgets.QDoubleSpinBox(self.widget)
        self.tweetCount.setDecimals(0)
        self.tweetCount.setMinimum(10.0)
        self.tweetCount.setMaximum(200.0)
        self.tweetCount.setObjectName("tweetCount")
        self.horizontalLayout.addWidget(self.tweetCount)
        self.getTweets = QtWidgets.QPushButton(self.widget)
        self.getTweets.setObjectName("getTweets")
        self.horizontalLayout.addWidget(self.getTweets)
        get_tweets.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(get_tweets)
        self.statusbar.setObjectName("statusbar")
        get_tweets.setStatusBar(self.statusbar)

        self.retranslateUi(get_tweets)
        QtCore.QMetaObject.connectSlotsByName(get_tweets)

    def retranslateUi(self, get_tweets):
        _translate = QtCore.QCoreApplication.translate
        get_tweets.setWindowTitle(_translate("get_tweets", "MainWindow"))
        self.label.setText(_translate("get_tweets", "Twitter NLP Utilities"))
        self.label_2.setText(_translate("get_tweets", "User handler:"))
        self.label_3.setText(_translate("get_tweets", "Tweet count:"))
        self.getTweets.setText(_translate("get_tweets", "Get Tweets"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    get_tweets = QtWidgets.QMainWindow()
    ui = Ui_get_tweets()
    ui.setupUi(get_tweets)
    get_tweets.show()
    sys.exit(app.exec_())

