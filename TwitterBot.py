# NOTE: to stop the stream, hit control + shift + \

# TODO:
# 1. handle exceptions given when parsing a tweet that's already been liked/favorited/followed/etc.
# 2. track DM's (most contests contact winners through DM)
# 3. figure out a way to leave this up and running forever (deal with rate limits?)
# 4. decide if we want to filter by location, language, etc.
# 5. waaaaaay down the road: we should unfollow/delete tweets/etc. like 2 weeks after we originally tweet.
#    most contests don't actually last that long.
# 6. handle cases where tweets tell us to follow someone else in order to be entered.
# 7. we really need to come up with a system to stream tweets now and parse later.
# 8. make our page look less bot-like.
# 9. STOP RETWEETING TWEETS THAT ARE JUST OTHER PEOPLE RETWEETING TRYING TO WIN SOMETHING.
#    maybe we save the message text somewhere and check if we've already retweeted a similar thing?
# 10. only retweet tweets from the current time period on. the stream occasionally returns stuff
#     from a couple weeks ago for some reason.
# 11. figure out which of our searches yeilds best results.
# just hit the follow limit...gotta make sure we're following and unfollowing the right people.

import tweepy
from keys import consumer_key, consumer_secret, access_token_key, access_token_secret
from db_handlers import TweetStorage

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)


# testing streams
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        #TweetStorage().add_to_db(status)
        import ipdb; ipdb.set_trace()
        print status.text
        return False
        # rudimentary error handling. following isn't working like at all, which sucks because
        # it's a common request. what gives?
        # separated into separate blocks to see if that helps with the following problem.
        # getting a huge amount of tweets in the stream that we've already retweeted/followed/liked.

    def retweet(self, status):
        try:
            api.retweet(status.id)
        except tweepy.TweepError as e:
            print e.message

    def favorite(self, status):
        try:
            api.create_favorite(status.id)
        except tweepy.TweepError as e:
            print e.message

    def follow(self, status):
        try:
            api.create_friendship(status.author.screen_name)
            print "followed successfully"
        except tweepy.TweepError as e:
            print e.message

    # ideally we'd get some sort of twilio notification or something when we've hit our rate limits.
    def on_error(self, status_code):
        if status_code == 420:  # if we overdo our rate limit
            print("Overdid our rate limit!")
            return False


class TwitterStream():

    TERMS = [
             'retweet follow chance win',
             'retweet like win',
             'giveaway like retweet win',
            ]

    def __init__(self):
        myStreamListener = MyStreamListener()
        self.myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    def filter_with(self, terms):
        self.myStream.filter(track=terms, async=True)

# so here's the deal. tweepy can't track and filter by location simultaneously.
# so it seems like we might want to dump this data out to a file and then read it and parse it later
# which isn't quite as clean of a solution but oh well...
# parameters in the same string must have all terms in order to return.
# different strings work on an either/or basis. if any string matches, the tweet is returned.

# other terms we should look for: giveaway, freebie, free stuff, ????
stream = TwitterStream()
stream.filter_with(stream.TERMS)


# miscellaneous:
# limit to san francisco airport:
# stream_SFO = stream_all.filter(locations=[-122.75,36.8,-121.75,37.8])
