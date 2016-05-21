# NOTE: to stop the stream, hit control + shift + \

# TODO:
# [x] handle exceptions given when parsing a tweet that's already been liked/favorited/followed/etc.
# [] track DM's (most contests contact winners through DM)
# [] figure out a way to leave this up and running forever (deal with rate limits?)
# [] decide if we want to filter by location, language, etc.
# [] we really need to come up with a system to stream tweets now and parse later.
# [x] make our page look less bot-like (not really programming-related).
# [] only retweet tweets from the current time period on. the stream occasionally returns stuff from a while back that we don't want to deal with.
# [x] don't retweet tweets that are just someone else retweeting the contest.
# [] deal with this embedded tweet nonsense
# [] parse @ signs
# [x] sleep when over rate limit
# [] pass in error rather than code #

import tweepy
import time
from keys import consumer_key, consumer_secret, access_token_key, access_token_secret
from db_handlers import TweetStorage

# global variable of bot spotters
spotters = ["BotSpotterBot"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

# begin class definition
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):

        tweet_to_retweet = self.get_og_tweet(status)
        self.retweet(tweet_to_retweet)
        self.favorite(tweet_to_retweet)
        self.follow(tweet_to_retweet)

    # returns a status object (earliest tweet we can find)
    def get_og_tweet(self, status):
        tweet_status = status
        while hasattr(tweet_status, 'retweeted_status'):
            tweet_status = tweet_status.retweeted_status
        return tweet_status

    def check_for_words(self, words, status):
        status.text = status.text.lower().replace("/", " ").replace(
                                                  ",", " ").replace("\\", " ")
        for word in words:
            if word in status.text:
                return True
        return False

    def check_if_bot_spotter(self, name):
        return (name in spotters)

    def retweet(self, status):
        if check_if_bot_spotter(status.author.screen_name):
            print("Caught a bot! " + status.author.screen_name)
            return

        words_to_check = ["retweet", "rt"]

        if self.check_for_words(words_to_check, status):
            try:
                api.retweet(status.id)
            except tweepy.TweepError as e:
                # print e.message
                self.on_error(e.message[0]['code'])

    def favorite(self, status):
        if check_if_bot_spotter(status.author.screen_name):
            print("Caught a bot! " + status.author.screen_name)
            return

        words_to_check = ["like", "favorite", "fave"]

        if self.check_for_words(words_to_check, status):
            try:
                api.create_favorite(status.id)
            except tweepy.TweepError as e:
                # print e.message
                self.on_error(e.message[0]['code'])

    def follow(self, status):
        if check_if_bot_spotter(status.author.screen_name):
            print("Caught a bot! " + status.author.screen_name)
            return

        words_to_check = ["follow"]

        if self.check_for_words(words_to_check, status):
            try:
                api.create_friendship(status.author.screen_name)
            except tweepy.TweepError as e:
                # print e.message
                self.on_error(e.message[0]['code'])

    def on_error(self, status_code):
        if status_code == 420:
            print("Overdid our rate limit! Taking a nap now...")
            time.sleep(60*15) # sleep for 15 minutes for new requests
            return False
        elif status_code == 327: # could we do a switch statement here instead?
            print("We have already retweeted that tweet.")
            return False
        elif status_code == 139:
            print("We have already favorited that tweet.")
            return False
        else:
            print("Encountered an error I don't know how to handle. Taking a nap...");
            print status_code
            time.sleep(60*15)
            return False


class TwitterStream():
    # class member to hold things we want to see
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
