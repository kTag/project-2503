import tweepy
import os

# Authentication 
client = tweepy.Client(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
)

response = client.search_recent_tweets("Tweepy")
# The method returns a Response object, a named tuple with data, includes,
# errors, and meta fields
print(response.meta)

# In this case, the data field of the Response returned is a list of Tweet
# objects
tweets = response.data

# Each Tweet object has default ID and text fields
for tweet in tweets:
    print(tweet.id)
    print(tweet.text)
