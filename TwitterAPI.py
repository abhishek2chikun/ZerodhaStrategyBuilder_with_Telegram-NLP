import re
import requests
import pandas as pd
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import snscrape.modules.twitter as sntwitter
import nltk
import sys
import datetime
import time
nltk.download('vader_lexicon')

def Sentiment(Symbols):
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAWeZAEAAAAA1p6ywlHOjj5iTAdWv%2BQtuPCffZY%3DuTM5N3k1EHtiN0MDnWZZ4j4Qkj1Gp1BXueHIArRJOQTCMtJkbO'
    Positive_list = []
    Negative_list = []
    Neutral_list = []
    for symbol in Symbols[:5]:
        
        params = {
            'q': symbol,
            'tweet_mode': 'extended',
            'lang': 'en',
            'count': '100'
        }
        response = requests.get('https://api.twitter.com/1.1/search/tweets.json',
            params=params,
            headers={'authorization': 'Bearer '+bearer_token})

        def get_data(tweet):
            data = {
                'id': tweet['id_str'],
                'created_at': tweet['created_at'],
                'text': tweet['full_text']
            }
            return data

        df = pd.DataFrame()
        for tweet in response.json()['statuses']:
            row = get_data(tweet)
            df = df.append(row, ignore_index=True)
        print(df.head())
        print(df.shape)
        def cleanTxt(text):
            text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
            text = re.sub('#', '', text) # Removing '#' hash tag
            text = re.sub('RT[\s]+', '', text) # Removing RT
            text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
            return text

        #applying this function to Text column of our dataframe
        df["text"] = df["text"].apply(cleanTxt)
        # print(df.head())



        #Sentiment Analysis
        def percentage(part,whole):
            return 100 * float(part)/float(whole)

        #Assigning Initial Values
        positive = 0
        negative = 0
        neutral = 0
        #Creating empty lists
        tweet_list1 = []
        neutral_list = []
        negative_list = []
        positive_list = []

        #Iterating over the tweets in the dataframe
        for tweet in df['text']:
            tweet_list1.append(tweet)
            analyzer = SentimentIntensityAnalyzer().polarity_scores(tweet)
            neg = analyzer['neg']
            neu = analyzer['neu']
            pos = analyzer['pos']
            comp = analyzer['compound']

            if neg > pos:
                negative_list.append(tweet) #appending the tweet that satisfies this condition
                negative += 1 #increasing the count by 1
            elif pos > neg:
                positive_list.append(tweet) #appending the tweet that satisfies this condition
                positive += 1 #increasing the count by 1
            elif pos == neg:
                neutral_list.append(tweet) #appending the tweet that satisfies this condition
                neutral += 1 #increasing the count by 1 

        positive = percentage(positive, len(df)) #percentage is the function defined above
        negative = percentage(negative, len(df))
        neutral = percentage(neutral, len(df))
        #Converting lists to pandas dataframe
        tweet_list1 = pd.DataFrame(tweet_list1)
        neutral_list = pd.DataFrame(neutral_list)
        negative_list = pd.DataFrame(negative_list)
        positive_list = pd.DataFrame(positive_list)
        #using len(length) function for counting
        # print("Since " + noOfDays + " days, there have been", len(tweet_list1) ,  "tweets on " + query, end='\n*')
        # print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n*')
        # print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n*')
        # print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n*')
        Positive_list.append(len(positive_list))
        Negative_list.append(len(negative_list))
        Neutral_list.append(len(neutral_list))

    df = pd.DataFrame({'Symbol':Symbols,'Positive %':Positive_list,'Negative %':Negative_list,'Neautral %':Neutral_list})
    print(df)
    df.to_csv('./Trend.csv',index=False)


while True:
    with open('./token.json','r') as f:
        Token = json.load(f)

    now = datetime.datetime.now()
    print(now.hour,now.minute)
    if (now.hour >= 15 and now.minute >= 30):
        print("Market Closed")
        
        sys.exit()
    if (now.hour >= 9 and now.minute >= 14 ):
        Sentiment(list(Token.values()))
        time.sleep(60*10)
