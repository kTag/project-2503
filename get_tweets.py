import tweepy

# Authentication 
client = tweepy.Client(
    consumer_key=${{ secrets.TWITTER_CONSUMER_KEY }},
    consumer_secret=${{ secrets.TWITTER_CONSUMER_SECRET }},
    access_token=${{ secrets.TWITTER_ACCESS_TOKEN }},
    access_token_secret=${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
)

# Fetch tweets
username = "woonomic"
tweets = client.get_users_tweets(username)

# Process tweets
for tweet in tweets.data:
    print(tweet.text)
