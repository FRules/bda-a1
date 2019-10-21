from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


MONGO_HOST = 'mongodb://localhost/test'

# Change your hashtags here
WORDS = ['#SGEB04', '#RBLWOB', '#SVWBSC',
         '#F95M05', '#FCAFCB', '#FCUSCF',
         '#BVBBMG', '#KOESCP', '#TSGS04']


class StreamListener(tweepy.StreamListener):

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        try:
            client = MongoClient(MONGO_HOST)
            
            # Use test database. If it doesn't exist, it will be created.
            db = client.test

            datajson = json.loads(data)

            created_at = datajson['created_at']
            username = datajson['user']['screen_name']
            text = datajson['text']

            print("Tweet collected at " + str(created_at) + " from user @" + username + ": " + text)

            db.twitterBundesliga.insert(datajson)
        except Exception as e:
           print(e)


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)


