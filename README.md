# twitter-NLP (WIP Thanks for your patience)
NLP (Natural Language Processing) for twitter

## What does it do?
NLP for twitter is a collection of routines that will allow the user to download the tweets of an specific user
and run NLP (Natural Language Processing) analysis.

The results will include:
- Word count
- Sentence count
- Vocabulary richnness
- Number of stopwords used
- Estimated text reading time
- Most common words 
- Sentiment analysis
- Setniment analysis scatter plot
- Word cloud chart

## What do you need?
Libraries:
- Python 3.0 or higher
- Twython
- NLTK
- Textblob
- Wordcloud

Twitter:
- consumer_key 
- consumer_secret 
- access_token 
- access_token_secret 

## Configuration:
Create a file with the name auth.py 
add the following lines: 
consumer_key = 'your consumer key' 
consumer_secret = 'your consumer secret' 
access_token = 'your access token' 
access_token_secret = 'your token secret' 

That´s it!

## Usage:
To dowload tweets:
python tweets_get.py --user <twitter_user> [--count <number_of_tweets>]  
note: the maximum number of tweets is 200  
 
To analyze tweet sentiment:  
USAGE: python tweets_sentiment.py --file <tweets_file.csv>  

To perform text analysis on tweets:  
python tweets_text_analysis.py --file <tweets_file.csv> --lang <en|es>  
  
To plot sentiment scatter chart:  
python tweets_scatter.py --file <tweets_file.csv>  
