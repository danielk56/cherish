import praw
import pybase64
import streamlit as st
import numpy as np # linear algebra
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS
import tweepy
import time
import csv


def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = pybase64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


st.title('Reddit: Parenting')

reddit = praw.Reddit(client_id='Cvc5Xh3ebOcyNg', client_secret='l0qVRCa22tFBExydOqHCH8b8z7I', user_agent='webscrape')

posts = []
ml_subreddit = reddit.subreddit('Parenting')
for post in ml_subreddit.hot(limit=30):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
print(posts)

posts.to_csv('reddit.csv', index=False)

#mpl.rcParams['figure.figsize']=(8.0,6.0)    #(6.0,4.0)
mpl.rcParams['font.size']=12                #10
mpl.rcParams['savefig.dpi']=100             #72
mpl.rcParams['figure.subplot.bottom']=.1

stopwords = set(STOPWORDS)
stopwords.update(['Everything', 'https', 'co', 'RT', 'therof', 'good', 'extremely', 'lot', 'for', 'that', 'have', 'your', 'everything'])
data = pd.read_csv("reddit.csv")


st.dataframe(data)

tmp_download_link = download_link(posts, 'YOUR_DF.csv', 'Click here to download your data!')
st.markdown(tmp_download_link, unsafe_allow_html=True)


wordcloud = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40,
                          collocations=False,
                          random_state=42
                         ).generate(str(data['title']))


print(wordcloud)
fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
fig.savefig("word1.png", dpi=900)
st.image("word1.png", use_column_width=True, caption= 'Wordcloud for Parenting Subreddit')


st.title('Reddit: Parenting Teenagers')

reddit = praw.Reddit(client_id='Cvc5Xh3ebOcyNg', client_secret='l0qVRCa22tFBExydOqHCH8b8z7I', user_agent='webscrape')

posts1 = []
ml1_subreddit = reddit.subreddit('parentingteenagers')
for post1 in ml1_subreddit.hot(limit=30):
    posts1.append([post1.title, post1.score, post1.id, post1.subreddit, post1.url, post1.num_comments, post1.selftext, post1.created])
posts1 = pd.DataFrame(posts1,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
print(posts1)

posts1.to_csv('reddit1.csv', index=False)

#mpl.rcParams['figure.figsize']=(8.0,6.0)    #(6.0,4.0)
mpl.rcParams['font.size']=12                #10
mpl.rcParams['savefig.dpi']=100             #72
mpl.rcParams['figure.subplot.bottom']=.1


data1 = pd.read_csv("reddit1.csv")

st.dataframe(data1)

tmp_download_link1 = download_link(posts1, 'YOUR_DF1.csv', 'Click here to download your data!')
st.markdown(tmp_download_link1, unsafe_allow_html=True)


wordcloud1 = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40,
                          collocations=False,
                          random_state=42
                         ).generate(str(data1['title']))


print(wordcloud1)
fig = plt.figure(1)
plt.imshow(wordcloud1)
plt.axis('off')
plt.show()
fig.savefig("word2.png", dpi=900)
st.image("word2.png", use_column_width=True, caption= 'Wordcloud for Parenting Teenagers Subreddit')


st.title('Google Trends: Parenting')

pytrend = TrendReq()
pytrend.build_payload(kw_list=['Parenting'])
related_queries = pytrend.related_queries()


with open('output.csv', 'w') as csv_file:
   csvwriter = csv.writer(csv_file, delimiter='\t')
   for type in related_queries:
      for query in related_queries[type]:
         csvwriter.writerow([query, related_queries[type][query]])

data = pd.read_csv('output.csv')
st.write(data)



st.title('Twitter: Parenting')

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

st.write(tweetsdf)


tmp_download_link2 = download_link(tweetsdf, 'YOUR_DF.csv', 'Click here to download your data!')
st.markdown(tmp_download_link2, unsafe_allow_html=True)

wordcloud1 = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40,
                          collocations=False,
                          random_state=42
                         ).generate(str(tweetsdf['Text']))


print(wordcloud1)
fig = plt.figure(1)
plt.imshow(wordcloud1)
plt.axis('off')
plt.show()
fig.savefig("word2.png", dpi=900)
st.image("word2.png", use_column_width=True, caption= 'Wordcloud for Parenting Tweets')