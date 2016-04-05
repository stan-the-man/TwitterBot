import twitter

# following installation instructions here

consumer_key="ebdjCz61Q7GYlVrr5XB9ogpbT"
consumer_secret="i6nQpX3RMQ9FWNFCp2UxOSVLyyTwnY4tjTvjjAtEftORGpCFTr"
access_token_key="717381819583180800-uGRzcyfbFcTHPG6PMtA8LrarPGWkdjb"
access_token_secret="qbtkTJAPfdbNdSlws1FLXE2DkCgwg0GaTHUB0c1K32UgQ"

class twitterBot():

    def __init__(self):
        self.consumer_key = "ebdjCz61Q7GYlVrr5XB9ogpbT"
        self.consumer_secret = "i6nQpX3RMQ9FWNFCp2UxOSVLyyTwnY4tjTvjjAtEftORGpCFTr"
        self.access_token_key = "717381819583180800-uGRzcyfbFcTHPG6PMtA8LrarPGWkdjb"
        self.access_token_secret = "qbtkTJAPfdbNdSlws1FLXE2DkCgwg0GaTHUB0c1K32UgQ"
        self.user_name = "ultron9000"

    def get_api(self):
        return twitter.Api(consumer_key=self.consumer_key,
                           consumer_secret=self.consumer_secret,
                           access_token_key=self.access_token_key,
                           access_token_secret=self.access_token_secret)


# test of verifying credentials. it works.
api = twitter.Api(consumer_key="ebdjCz61Q7GYlVrr5XB9ogpbT",
                  consumer_secret="i6nQpX3RMQ9FWNFCp2UxOSVLyyTwnY4tjTvjjAtEftORGpCFTr",
                  access_token_key="717381819583180800-uGRzcyfbFcTHPG6PMtA8LrarPGWkdjb",
                  access_token_secret="qbtkTJAPfdbNdSlws1FLXE2DkCgwg0GaTHUB0c1K32UgQ")



#results = api.GetSearch(geocode=[37.781157, -122.398720, "1mi"]

#results = api.GetSearch(term="retweet follow like chance win", count=1)
#print([s.text + "\n\n" for s in results])


# tweepy tests
import tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

#results = api.search('retweet follow like chance win')
#print results[0].author.screen_name

# testing streams


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        if status_code == 420:
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['chance win'], async=True)
