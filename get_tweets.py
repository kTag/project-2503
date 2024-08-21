import tweepy
import os

# Authentication 
client = tweepy.Client(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
)

# Fetch tweets
username = '630092237' 
tweets = client.get_users_tweets(id=username, tweet_fields=['context_annotations','created_at','geo'])

# Process tweets
for tweet in tweets.data:
    print(tweet.text)
