# NOTE: to stop the stream, hit control + shift + \

# tweepy tests
import tweepy
import json
from keys import consumer_key, consumer_secret, access_token_key, access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

#results = api.search('retweet follow like chance win')
#print results[0].author.screen_name

# testing streams
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text
        # api.retweet(status.id)

        # here gotta parse the message
        # if 'retweet' in status.text and 'like' in status.text and 'follow' in status.text and 'win' in status.text:
        #     print status.text
        #api.favorite(status.id)
        # print status.id

    def on_error(self, status_code):
        if status_code == 420: # if we overdo our rate limit
            print("Overdid our rate limit!")
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# so here's the deal. tweepy can't track and filter by location simultaneously.
# so it seems like we gotta dump this data out to a file and then read it and parse it later
# which isn't quite as clean of a solution but oh well...
# also note that this track parameter matches any of these terms, not all of them.
# so maybe we could pad it out with a couple custom phrases.
myStream.filter(track=['retweet', 'like', 'follow', 'chance', 'win'], async=True)

# now we gotta find out how to iterate through these tweets and do cool things with them
# limit to san francisco airport:
# stream_SFO = stream_all.filter(locations=[-122.75,36.8,-121.75,37.8])
