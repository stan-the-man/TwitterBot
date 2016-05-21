from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tweepy.models import Status

Base = declarative_base()
engine = create_engine('sqlite:///embedded_tweet.db', echo=False)


class Twitters(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    tweet_id = Column(Integer)
    author_screen_name = Column(String)

    def __repr__(self):
        return '<Twitters(text= %s, tweet_id= %i, author_screen_name= %s)>' % (self.text, self.tweet_id, self.author)


class TweetStorage():

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    def add_to_db(self, tweet):
        new_tweet = Twitters(text=tweet.text, tweet_id=tweet.id,
                             author_screen_name=tweet.author.screen_name)
        session = self.Session()
        session.add(new_tweet)
        session.commit()
        session.close()

    def find_tweet_by_id(self, id):
        session = self.Session()
        tweets = session.query(Twitters).filter_by(id=id).first()
        session.close()
        return tweets

    def first_ten_tweets(self):
        session = self.Session()
        tweets = session.query(Twitters)
        return tweets[0:10]

