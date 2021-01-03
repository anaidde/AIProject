import tweepy
import json

CONSUMER_KEY = "complete-with-your-keys"
CONSUMER_SECRET = "complete-with-your-keys"
OAUTH_TOKEN = "complete-with-your-keys"
OAUTH_TOKEN_SECRET = "complete-with-your-keys"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

jsonBody = open('tweets.json', 'r').read()
tweetJson = json.loads(jsonBody)

updatedTweetInfo = []

count = 0
for tweetInfo in tweetJson['tweets']:
    try:
        id = tweetInfo['i']
        tweet = api.get_status(id)
        print(tweet.retweet_count, tweet.favorite_count, flush=True)
        tweetInfo.update({"i": count, "rt": tweet.retweet_count, "fc": tweet.favorite_count})
        count += 1
        updatedTweetInfo.append(tweetInfo)
    except Exception as e:
        print(e)
    

updatedTweets = {
    "tweets": updatedTweetInfo
}

g = open('updatedTweets.json', 'w')

g.write( json.dumps(updatedTweets) )



