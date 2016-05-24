import pytz
import re
from datetime import datetime
import urllib2

# this code is copied from http://stackoverflow.com/questions/6500721/find-where-a-t-co-link-goes-to
class HeadRequest(urllib2.Request):
    def get_method(self): return "HEAD"

# this code is copied from http://stackoverflow.com/questions/6500721/find-where-a-t-co-link-goes-to
def get_real(url):
    res = urllib2.urlopen(HeadRequest(url))
    return res.geturl()

def parse_lengthened_url(url):
    return re.search(r'/status/(\d+)', url).group(1)

def get_embedded_tweet(url):
    long_url = get_real(url)
    return parse_lengthened_url(long_url)

def get_now():
    return pytz.utc.localize(datetime.now())

def bot_in_name(name):
    return bool(re.search(r'botspotter', name.lower()))
