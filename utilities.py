import pytz
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
    except ConnectionError as e:
        print e

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
