from utilities import *

def test_bot_in_name():
    assert bot_in_name('RealBotSpotter')
    assert not bot_in_name('GiveawayBot')

def test_parse_long_url():
    url = 'https://twitter.com/shanselman/status/276958062156320768/photo/1'
    tweet_id = '276958062156320768'
    assert parse_lengthened_url(url) == tweet_id

def test_embedded_tweet():
    url = 'http://t.co/yla4TZys'
    real_tweet_id = '276958062156320768'
    assert get_embedded_tweet(url) == real_tweet_id

# run tests here:
test_bot_in_name()
test_parse_long_url()
test_embedded_tweet()
