#Uses tweepy api to extract tweets with certain keywords or hashtags https://github.com/tweepy/tweepy
import time, tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#OAuth information from Twitter API
consumer_key = input('Consumer key: ')
consumer_secret = input('Consumer secret: ')
access_token = input('Access token: ')
access_secret = input('Access secret: ')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

class Listener(StreamListener):
    def on_data(self, data):
        try:
            # Save raw data in text file
            saveFile = open('twitterDB_raw.txt', 'a')
            saveFile.write(data)
            saveFile.write('\n')
            saveFile.close()
            
            post_time = data.split('{\"created_at\":\"')[1].split('\",\"id\":')[0]
            post_id = data.split('\"user\":{\"id\":')[1].split(',\"id_str\":')[0]
            post_text = data.split('\"text\":\"')[1].split(',\"source')[0]
            user = api.get_user(post_id)
            tweet = user.name + " (@" + user.screen_name + ") posted on " + post_time + ": " + post_text
            
            #Save filtered tweets in separate text file and print out tweets
            print("\n\n" + tweet)
            saveFile = open('twitterDB.txt', 'a')
            saveFile.write(tweet)
            saveFile.write('\n\n')
            saveFile.close()
            
            return True
        except (BaseException, e):
            print('failed on_data: ' + str(e))
            time.sleep(5)

def on_error(self, status):
    print("Twitter Error: " + status)
    if status == 420:
        # returning False in on_data disconnects the stream
        return False


twitter_stream = Stream(auth, Listener())
#List of keywords to filter and track
twitter_stream.filter(track=['Fortnite','Epic Games'])
