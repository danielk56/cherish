import tweepy
import time
import pandas as pd


consumer_key = "ClNjbpTV88lKnhqyVShXN9ym0"
consumer_secret = "tkWLEHeVWQbQTfoqXXUVePDNqQBqfB9wxU46V17XBlXvS3qKxz"
access_token = "1278402455261364227-nKSeo4xB6N67vgBJMvDMVmQTSVf6ig"
access_token_secret = "dQ89evCijXCzZTQQzLUQCOZs36EZbXEriNNblsZ9nv05l"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


tweets = []
text_query = 'Parenting'
count = 100
try:
# Pulling individual tweets from query
    for tweet in api.search(q=text_query, count=count):
# Adding to list that contains all tweets
      tweets.append((tweet.created_at,tweet.id,tweet.text))
      tweetsdf = pd.DataFrame(tweets,columns=['Datetime', 'Tweet Id', 'Text'])
      tweetsdf.to_csv('{}-tweets.csv'.format(text_query))
except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)

print(tweetsdf)