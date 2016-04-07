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
# 9. STOP RETWEETING TWEETS THAT ARE JUST OTHER PEOPLE RETWEETING TRYING TO WIN SOMETHING

import tweepy
import json # not sure if necessary
from keys import consumer_key, consumer_secret, access_token_key, access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

# testing streams
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text
        """ dir(status) returns the following:
        ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__',
        '__getstate__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__',
        '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
        '__weakref__', '_api', '_json', 'author', 'contributors', 'coordinates', 'created_at',
        'destroy', 'entities', 'extended_entities', 'favorite', 'favorite_count', 'favorited',
        'filter_level', 'geo', 'id', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
        'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'is_quote_status',
        'lang', 'parse', 'parse_list', 'place', 'possibly_sensitive', 'retweet', 'retweet_count',
        'retweeted', 'retweeted_status', 'retweets', 'source', 'source_url', 'text',
        'timestamp_ms', 'truncated', 'user'] """

        """ status.author returns (random example)
        User(follow_request_sent=None, profile_use_background_image=True,
        _json={u'follow_request_sent': None, u'profile_use_background_image': True,
        u'default_profile_image': False, u'id': 2781052820, u'verified': False,
        u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/673978468162400256/rf4zqEiq_normal.jpg',
         u'profile_sidebar_fill_color': u'C0DFEC', u'profile_text_color': u'333333',
         u'followers_count': 7603, u'profile_sidebar_border_color': u'A8C7F7',
         u'id_str': u'2781052820', u'profile_background_color': u'022330',
         u'listed_count': 861,
         u'profile_background_image_url_https': u'https://abs.twimg.com/images/themes/theme15/bg.png',
         u'utc_offset': -25200, u'statuses_count': 251619, u'description': u'Is my fastpass ready yet?',
         u'friends_count': 2448, u'location': u'Anaheim, CA', u'profile_link_color': u'0084B4',
         u'profile_image_url': u'http://pbs.twimg.com/profile_images/673978468162400256/rf4zqEiq_normal.jpg',
         u'following': None, u'geo_enabled': False,
         u'profile_banner_url': u'https://pbs.twimg.com/profile_banners/2781052820/1449714643',
         u'profile_background_image_url': u'http://abs.twimg.com/images/themes/theme15/bg.png',
         u'name': u'Katia', u'lang': u'en', u'profile_background_tile': False, u'favourites_count': 6313,
         u'screen_name': u'redk3tchup', u'notifications': None, u'url': None,
         u'created_at': u'Sat Aug 30 20:02:26 +0000 2014', u'contributors_enabled': False,
         u'time_zone': u'Pacific Time (US & Canada)', u'protected': False, u'default_profile': False,
         u'is_translator': False}, id=2781052820, _api=<tweepy.api.API object at 0x10c607190>,
          verified=False, profile_image_url_https=u'https://pbs.twimg.com/profile_images/673978468162400256/rf4zqEiq_normal.jpg',
          profile_sidebar_fill_color=u'C0DFEC', is_translator=False, geo_enabled=False,
          profile_text_color=u'333333', followers_count=7603, protected=False, location=u'Anaheim, CA',
          default_profile_image=False, id_str=u'2781052820', utc_offset=-25200, statuses_count=251619,
          description=u'Is my fastpass ready yet?', friends_count=2448, profile_link_color=u'0084B4',
          profile_image_url=u'http://pbs.twimg.com/profile_images/673978468162400256/rf4zqEiq_normal.jpg',
          notifications=None,
          profile_background_image_url_https=u'https://abs.twimg.com/images/themes/theme15/bg.png',
          profile_background_color=u'022330',
          profile_banner_url=u'https://pbs.twimg.com/profile_banners/2781052820/1449714643',
          profile_background_image_url=u'http://abs.twimg.com/images/themes/theme15/bg.png',
          screen_name=u'redk3tchup', lang=u'en', profile_background_tile=False, favourites_count=6313,
          name=u'Katia', url=None, created_at=datetime.datetime(2014, 8, 30, 20, 2, 26),
          contributors_enabled=False, time_zone=u'Pacific Time (US & Canada)',
          profile_sidebar_border_color=u'A8C7F7', default_profile=False, following=False, listed_count=861)"""

        # rudimentary error handling. following isn't working like at all, which sucks because
        # it's a common request. what gives?
        # separated into separate blocks to see if that helps with the following problem.
        try:
            api.retweet(status.id)
        except tweepy.TweepError as e:
            print e.message
        try:
            api.create_favorite(status.id)
        except tweepy.TweepError as e:
            print e.message
        try:
            api.create_friendship(status.author.screen_name)
            print "followed successfully"
        except tweepy.TweepError as e:
            print e.message
        """try:
            api.retweet(status.id) # retweet the status first
            api.create_favorite(status.id) # then favorite the status
            api.create_friendship(status.author.screen_name) # then follow the user
            print status.author.screen_name
            print "tweet dealt with successfully" # this rarely triggers because following is messed up.
        except tweepy.TweepError as e: # catch those errors
            print e.message"""


    # ideally we'd get some sort of twilio notification or something when we've hit our rate limits.
    def on_error(self, status_code):
        if status_code == 420: # if we overdo our rate limit
            print("Overdid our rate limit!")
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# so here's the deal. tweepy can't track and filter by location simultaneously.
# so it seems like we might want to dump this data out to a file and then read it and parse it later
# which isn't quite as clean of a solution but oh well...
# parameters in the same string must have all terms in order to return.
# different strings work on an either/or basis. if any string matches, the tweet is returned.

# other terms we should look for: giveaway, freebie, free stuff, ????
myStream.filter(track=['retweet follow chance win', 'retweet like win', 'giveaway like retweet win'], async=True) # anecdotally good search terms

# miscellaneous:
# limit to san francisco airport:
# stream_SFO = stream_all.filter(locations=[-122.75,36.8,-121.75,37.8])
