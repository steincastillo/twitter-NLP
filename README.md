# twitter-NLP (WIP Thanks for your patience)
**NLP (Natural Language Processing) python analyzer for twitter**  

**Important:** Please note that the GUI functionality is currently being added to the library. A branch has been created
for this effect. It will be promoted to the main branch soon. Thanks a lot for your patience.  

## What does it do?
NLP for twitter is a collection of routines that will allow the user to download the tweets of an specific user
and run NLP (Natural Language Processing) analysis.

The results will include:
- Wordcloud chart
- Sentiment scatter chart
- Tweet frequency chart
- Word count
- Sentence count
- Vocabulary richnness
- Number of stopwords used
- Number of profanity words
- Estimated text reading time
- Most common words 
- Sentiment analysis 

## What do you need?
**Libraries:**  
- Python 3.0 or higher
- Twython
- NLTK
- Textblob
- Wordcloud

**Twitter:**  
- consumer_key 
- consumer_secret 
- access_token 
- access_token_secret 

## Configuration:
Create a file with the name auth.py  
add the following lines:  
`consumer_key = 'your consumer key'`  
`consumer_secret = 'your consumer secret'`  
`access_token = 'your access token'`  
`access_token_secret = 'your token secret'`

If you need to create your consumer key click [here](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)  
  
That´s it!  
  
## Usage:
  
_To dowload tweets:_  
`python tweets_get.py --user <twitter_user> [--count <number_of_tweets>]`  
note: the maximum number of tweets is 200  
 
_To analyze tweet sentiment:_  
`python tweets_sentiment.py --file <tweets_file.json>`  

_To perform text analysis on tweets:_  
`python tweets_text_analysis.py --file <tweets_file.json> --lang <en|es>`  
  
_To plot sentiment scatter chart:_  
`python tweets_scatter_v2.py --file <tweets_file.json>`  

_To plot tweet sentiment and tweeting frequency:_  
`python tweets_graph.py --file <tweets_file.json>`  

_To listen to tweets:_  
`python tweets_listener.py --track <keyword> [--lang [en|es]]`  
note: the number of tweets to listen to is controlled by a coded constant. Adjust this value to your needs  

# Have a question or a suggestion? 
Feel free to add an issue to the repo or contact me at: contact@steincastillo.com 

## Profanity warning
Please be advised that this repository contains files with a list of profanity words used in english (EN) and spanish (ES).
The only purpose of these files is to conduct NLP research and analisys on texts and should be treated as such.
