import tweepy # for all the twitter junk
import time # for sleeping
import pytz # for date-checking
from urllib2 import HTTPError
from datetime import timedelta # for date-checking
from keys import (consumer_key, consumer_secret,
                  access_token_key, access_token_secret, SELF_SCREEN_NAME,
                  account_sid, auth_token, from_number, keegan_number, stan_number)
from db_handlers import TweetStorage
from utilities import (get_now, bot_in_name,
                       parse_embedded_tweet, create_logger, get_random_imgur)
import random # for randomly selecting a phrase for imgur link
from twilio.rest import TwilioRestClient

# global variable of bot spotters
spotters = ["BotSpotterBot", "RealBotSpotter", "bufbvr", "blkchninstitute", "Annaladygrande"]
MAX_DAYS_BACK = 3

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

# count=1 only returns the most recent one.
mentions = api.mentions_timeline(count=1)
for mention in mentions:
    print "Text: " + mention.text
    print "Sent by: " + mention.user.screen_name

# now open the file to see if it's the same mention we had last time.
f = open('mentions.txt', 'r+')
previous_mention = f.read()
if previous_mention != mentions[0].text: # if we got a new mention
    # now it's time to send a message with Twilio. eventually add Stan too.
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body="New @mention: " + mentions[0].text,
                    to=keegan_number,
                    from_=from_number)
    print(message.sid)
    # then update the file
    f.truncate() # to erase the file. THIS IS UNTESTED! 
    f.write(mentions[0].text)
f.close()

print mentions[0].text
print previous_mention

# construct a "random" tweet
string = get_random_imgur()
IMGUR_TERMS = [
      'haha so funny',
      'guys check this pic out',
      'this is great omg',
      'haha this is amazing',
      'can\'t even believe this pic haha',
      'what is this even about'
       ]

msg = random.choice(IMGUR_TERMS) + '\n' + string
print(msg)

# now let's post the tweet
def update(msg):
    try:
        api.update_status(msg)
    except:
        time.sleep(60*5) # sleep 5 minutes
        update(msg) # then try again

update(msg)
