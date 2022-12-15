from peewee import *

db = SqliteDatabase('tweets.db')


class TweetInitial(Model):
    name = CharField()
    tweet_text = CharField()
    country_code = CharField()
    display_url = CharField()
    lang = CharField()
    created_at = DateTimeField()
    location = CharField()

    class Meta:
        database = db


class User(Model):
    name = CharField()
    location = CharField()

    class Meta:
        database = db


class Language(Model):
    lang = CharField()

    class Meta:
        database = db


class Country(Model):
    country_code = CharField()

    class Meta:
        database = db


class TweetNormalized(Model):
    name = ForeignKeyField(User, backref='name_tweets')
    tweet_text = CharField()
    country = ForeignKeyField(Country, backref='country_tweets')
    display_url = CharField()
    lang = ForeignKeyField(Language, backref='lang_tweets')
    created_at = DateTimeField()
    tweet_sentiment = IntegerField(default=0)

    class Meta:
        database = db
