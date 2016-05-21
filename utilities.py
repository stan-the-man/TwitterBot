import pytz
from datetime import datetime

def get_now():
    return pytz.utc.localize(datetime.now())
