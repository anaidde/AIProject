"""
Code from:
https://5harad.com/mse331/assets/hw2/tweet_stream.py
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import argparse

keyFile = 'creds.txt'
totalTweets = 0

# read twitter app credentials
creds = {}
for line in open(keyFile, 'r'):
  key, value = line.rstrip().split()
  creds[key] = value

class listener(StreamListener):
  def on_data(self, tweet):
    global totalTweets
    myTweetJSON = json.loads(tweet)
    try:
        if not myTweetJSON['retweeted'] and not myTweetJSON["text"].startswith("RT @"):
            currentTweet = {
            "ca": myTweetJSON["created_at"],
            "i": myTweetJSON["id_str"],
            "t": myTweetJSON["text"],
            "y": {
                "fc" : myTweetJSON['user']["followers_count"],
                "frc" : myTweetJSON['user']["friends_count"],
                "lc" : myTweetJSON['user']["listed_count"],
                "fac" : myTweetJSON['user']["favourites_count"],
                "sc" : myTweetJSON['user']["statuses_count"]
            }
        }
            totalTweets += 1
            print("Nr: ", totalTweets, flush=True)
            with open("tweets.js", "a") as myFile:
                myFile.write( json.dumps(currentTweet) + ",\n" )
    except Exception as e:
        print(e, flush=True)
    
    """
        currentTweet = {
        "created_at": myTweetJSON["created_at"],
        "id_str": myTweetJSON["id_str"],
        "text": myTweetJSON["text"],
        "user": {
            "followers_count" : myTweetJSON['user']["followers_count"],
            "friends_count" : myTweetJSON['user']["friends_count"],
            "listed_count" : myTweetJSON['user']["listed_count"],
            "favourites_count" : myTweetJSON['user']["favourites_count"],
            "statuses_count" : myTweetJSON['user']["statuses_count"]
        }
    }
    """
    
  def on_error(self, status):
    print(status, flush=True)

# set up authentication
auth = OAuthHandler(creds['api_key'], creds['api_secret'])
auth.set_access_token(creds['token'], creds['token_secret'])

# set up stream
twitterStream = Stream(auth, listener())

filter = ["computer", "science"]

twitterStream.filter(track=['science'])