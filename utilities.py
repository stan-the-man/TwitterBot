import pytz
import logging
import re
from datetime import datetime
import urllib2

# this code is copied from http://stackoverflow.com/questions/6500721/find-where-a-t-co-link-goes-to
class HeadRequest(urllib2.Request):
    def get_method(self): return "HEAD"

# this code is copied from http://stackoverflow.com/questions/6500721/find-where-a-t-co-link-goes-to
def get_real(url):
    try:
        res = urllib2.urlopen(HeadRequest(url))
        return res.geturl()
    except:
        print "Error with get_real."
        return " "

# returns current time for logging purposes
def get_now():
    return pytz.utc.localize(datetime.now())

# returns a random imgur url to make us look less bot-like
def get_random_imgur():
    url = 'http://imgur.com/random'
    final_url = get_real(url)
    return final_url

# to check if 'botspotter' is in the name. not a super elegant solution right now.
# could be expanded to work with the names of other bots we know of.
def bot_in_name(name):
    return bool(re.search(r'botspotter', name.lower()))

# regex to check if we should retweet a different tweet rather than the one
# that tweepy's stream gives us (improves our accuracy)
def search_for_embedded_tweet(text):
    short_url = re.search(r'(t\.co\/)[\w\d]+', text)
    if short_url:
        return short_url.group(0)
    return None

# gives us the status number of the embedded tweet. called after search_for_embedded_tweet()
def parse_embedded_tweet(text):
    short_url = search_for_embedded_tweet(text)
    if short_url is None:
        return

    long_url = get_real('http://' + short_url)
    is_twitter = re.search(r'twitter.com', long_url)
    if not is_twitter:
        return

    id = re.search(r'/status/(\d+)', long_url)
    if id is None:
        return
    return id.group(1)

# returns a list. empty if nothing to be followed.
def if_follow_others(text):
    user_names = re.finditer(r'(\@)[\w\d]+', text)
    words = ["follow"]
    list_of_names = []
    if check_for_words(words, text):
        for match in user_names:
            # this is temporary. in the future we need to follow here.
            # maybe we return a tuple containing the names we need to follow?
            # print match.group(0)[1:]
            list_of_names.append(match.group()[1:])
    return list_of_names

# just doubled up check_for_words. it really should be here anyway.
def check_for_words(words, text):
    text = text.lower().replace("/", " ").replace(
                                              ",", " ").replace("\\", " ")
    for word in words:
        if word in text:
            return True
    return False


def create_logger(name):
    '''logging information. Taken from http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python'''
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    handler = logging.FileHandler(name + '.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


