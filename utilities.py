import pytz
import random
import logging
import re
from datetime import datetime
from const import IMGUR_TERMS
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

def get_now():
    return pytz.utc.localize(datetime.now())

def bot_in_name(name):
    return bool(re.search(r'botspotter', name.lower()))

def search_for_embedded_tweet(text):
    short_url = re.search(r'(t\.co\/)[\w\d]+', text)
    if short_url:
        return short_url.group(0)
    return None

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

# returns a random imgur url to make us look less bot-like
def get_random_imgur():
    url = 'http://imgur.com/random'
    final_url = get_real(url)
    return final_url + ' ' + random.choice(IMGUR_TERMS)
