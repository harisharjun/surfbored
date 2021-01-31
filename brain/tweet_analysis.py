#Importing Libraries required to run this program
import tweepy
#import sys
from textblob import TextBlob

#Main Function
def tweet_analysis_function(movie_name):
    #Assign keys required to access the Twitter API
    consumer_key = 'qB0sRd9boDNn3rlqNscSUzEAI'
    consumer_secret = 'lEnRYTVR4NgimdPmyC383GapBdw5cNwAB98H2Zak9kWEOICPr4'
    access_token='150188229-0VkVsjiu2oZ2kp44p48gsC6aO4NCYbz0abUXDJy8'
    access_token_secret='vrwK53SGlNJ3QCa7YCxQ2iGCQat5zxLfUZOXjgv4MN9Rt'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    #Function to print BMP Characters - not used in this program though
    '''
    def decode_bmp(text):
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        item=text.translate(non_bmp_map)+'\n\n'
        return item
    '''

    def is_it_a_movie(movie_name):
        regex="#{1}[a-zA-Z0-9]+[a-zA-Z0-9\s]"
        new_movie_name=""
        for i in movie_name:
            if i=="#":
                new_movie_name=movie_name(1,len(movie_name))
        
    #Sentiment Analysis using TextBlob

    def tweets_sentiment_count(tweets_analysis):
        count_positive=0.0
        count_negative=0.0
        count_neutral=0.0
        for i in tweets_analysis:
            if tweets_analysis[i]=='positive':
                count_positive+=1
            elif tweets_analysis[i]=='neutral':
                count_neutral+=1
            else:
                count_negative+=1
        count_sentiment=dict()
        count_sentiment['count_positive']=count_positive
        count_sentiment['count_neutral']=count_neutral
        count_sentiment['count_negative']=count_negative
        count_sentiment['movie_name']=movie_name
        return count_sentiment

    def tweets_sentiment(tweets_dict):
        tweet_analysis={}
        for tweet in tweets_dict:
            analysis=TextBlob(tweets_dict[tweet])
            if analysis.sentiment.polarity>0:
                tweet_analysis[tweet]='positive'
            elif analysis.sentiment.polarity==0:
                tweet_analysis[tweet]='neutral'
            else:
                tweet_analysis[tweet]='negative'
            #print(tweets_dict[tweet]+": "+tweet_analysis[tweet]+"\n\n")
        return tweet_analysis

    #Get Min ID:
    def get_min_id(public_tweets):
        dict1={}
        for i in public_tweets:
            dict1[i]=i
        return min(dict1.values())

#    def movie_checker(movie_name):
#        file=open('movies.txt','r')
#        for movie in file:
            
    #The Main Program
    count=1001
    temp=0
    last_tweet_id=""
    public_tweets={}
    #Loop to gather more than 100 tweets, as Twitter API returns only 100 tweets per request.
    while temp<count:
        
        if temp==0:
            if count<=100:
                temp_tweets = api.search(movie_name,count=count,tweet_mode="extended")
                for i in temp_tweets:
                    public_tweets[i.id_str]=i.full_text
                temp+=count
                last_tweet_id=get_min_id(public_tweets)
            elif count>100:
                temp_tweets = api.search(movie_name,count=100,tweet_mode="extended")
                for i in temp_tweets:
                    public_tweets[i.id_str]=i.full_text
                temp+=100
                last_tweet_id=get_min_id(public_tweets)
        elif temp>0:
            if count>100 and count-temp>100:
                temp_tweets = api.search(movie_name,count=100,tweet_mode="extended",max_id=last_tweet_id)
                for i in temp_tweets:
                    public_tweets[i.id_str]=i.full_text
                temp+=100
                last_tweet_id=get_min_id(public_tweets)
            elif count>100 and count-temp<=100:
                temp_tweets = api.search(movie_name,count=count-temp,tweet_mode="extended",max_id=last_tweet_id)
                for i in temp_tweets:
                    public_tweets[i.id_str]=i.full_text
                temp+=100
                last_tweet_id=get_min_id(public_tweets)

    print(len(public_tweets))

    tweets_dict={}
    i=1

    #Gathering Tweets and their IDs into a dict
    for tweet in public_tweets:
        tweets_dict[tweet]=public_tweets[tweet]
        tweets_dict[tweet]= ''.join(c for c in tweets_dict[tweet] if c <= '\uFFFF')
        #print(str(i)+" "+tweets_dict[tweet]+"\n")
        i+=1

    #Running the sentiment query
    count_sentiment=dict()
    count_sentiment=tweets_sentiment_count(tweets_sentiment(tweets_dict))
    

    #print('\nTotal Tweets Analyzed: '+str(i-1)) #i-1 will be equal to count

    c_pos=round(100.00*count_sentiment['count_positive']/(i-1),2)
    c_neu=round(100.00*count_sentiment['count_neutral']/(i-1),2)
    c_neg=round(100.00*count_sentiment['count_negative']/(i-1),2)
    #print(count_sentiment)

    #print('Used Twitter API and Python to analyze the latest '+str(count)+' tweets with '+ movie_name +' hashtag. And this is what the audiences feel:\nSuperb: '+str(c_pos)+'%\nAverage: '+str(c_neu)+'%\nBad: '+str(c_neg)+'%')
    
    return count_sentiment