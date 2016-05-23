import pytz
import re
from datetime import datetime

def get_now():
    return pytz.utc.localize(datetime.now())

def bot_in_name(name):
    return bool(re.search(r'botspotter', name.lower()))
