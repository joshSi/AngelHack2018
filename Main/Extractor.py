#Uses tweepy api to extract tweets with certain keywords or hashtags https://github.com/tweepy/tweepy
import time, argparse
from tweepy import Stream, OAuthHandler, API
from tweepy.streaming import StreamListener

#OAuth information for Twitter API

#Default if auth_api isn't called
api = API()

def auth_api(consumer_key, consumer_secret, access_token, access_secret):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = API(auth)
    return auth

def auth_stdin():
    c_key = input('Consumer key: ')
    c_secret = input('Consumer secret: ')
    a_token = input('Access token: ')
    a_secret = input('Access secret: ')
    return auth_api(c_key, c_secret, a_token, a_secret)

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

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ck", "--c_key", help="Consumer Key")
    parser.add_argument("-cs", "--c_secret", help="Consumer Secret")
    parser.add_argument("-at", "--a_token", help="Access Token")
    parser.add_argument("-ak", "--a_key", help="Access Key")
    parser.add_argument("-k", "--keyword", default = 'Hello World', help="Keyword to track (default: 'Hello World')")

    args = parser.parse_args()
    if (args['ck'] and args['cs'] and args['at'] and args['ak']):
        auth = auth_api(args['ck'], args['cs'], args['at'], args['ak'])
    else:
        auth = auth_stdin()
    twitter_stream = Stream(auth, Listener())
    #List of keywords to filter and track
    twitter_stream.filter(track=args['keyword'])
