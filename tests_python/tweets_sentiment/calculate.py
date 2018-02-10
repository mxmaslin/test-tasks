import json
import string

from peewee import *

from models import TweetInitial, TweetNormalized, Language, Country, User, db


def fill_tweet_table():
    counter = 0
    print('Start writing tweets to tweets table')
    with open('three_minutes_tweets.json.txt') as f:
        for tweet in f:
            tweet = json.loads(tweet)
            if 'user' in tweet:
                t = TweetInitial.create(
                    name=tweet['user']['name'],
                    tweet_text=tweet['text'],
                    country_code=tweet['place']['country_code'] if tweet['place'] else 'None',
                    display_url='https://twitter.com/statuses/{}'.format(tweet['id_str']),
                    lang=tweet['lang'],
                    created_at=tweet['created_at'],
                    location=tweet['user']['location'])
                t.save()
                counter += 1
                print('Tweet {} is written to tweetinitial table'.format(counter))
    print('{} tweets written to tweetinitial table'.format(counter))


def fill_user_table():
    user_query = (TweetInitial
        .select(TweetInitial.name, TweetInitial.location))
    counter = user_query.count()
    for user in user_query:
        User.create(
            name=user.name,
            location=user.location).save()
        counter -= 1
        message = 'Creating user, units remaining: {}'
        print(message.format(counter))


def fill_country_table():
    cc_query = (TweetInitial
        .select(TweetInitial.country_code)
        .distinct())
    counter = cc_query.count()
    for cc in cc_query:
        Country.create(
            country_code=cc.country_code).save()
        counter -= 1
        message = 'Creating country, units remaining: {}'
        print(message.format(counter))


def fill_language_table():
    lang_query = (TweetInitial
        .select(TweetInitial.lang)
        .distinct())
    counter = lang_query.count()
    for lang in lang_query:
        Language.create(lang=lang.lang).save()
        counter -= 1
        message = 'Creating language, units remaining: {}'
        print(message.format(counter))


def create_sentiment_dict():
    sentiment_dict = dict()
    with open('AFINN-111.txt') as f:
        lines = f.readlines()
        for line in lines:
            splitted = line.split()
            sentiment = ' '.join(splitted[:-1])
            value = splitted[-1]
            sentiment_dict[sentiment] = value
    return sentiment_dict


def calculate_tweet_sentiment(tweet, sentiment_dict):
    sentiment = 0
    translator = str.maketrans('', '', string.punctuation)
    tweet = tweet.translate(translator).lower().split()
    for word in tweet:
        if word in sentiment_dict:
            sentiment += int(sentiment_dict[word])
    return sentiment


def calculate_tweets_sentiment():
    print('Start calculating sentiments')
    sentiment_dict = create_sentiment_dict()
    tweets_initial = TweetInitial.select()
    counter = tweets_initial.count()
    for tweet in tweets_initial:
        user = (User
            .select()
            .where(User.name == tweet.name)
            .get())
        country = (Country
            .select()
            .where(Country.country_code == tweet.country_code)
            .get())
        lang = (Language
            .select(Language.id)
            .where(Language.lang == tweet.lang)
            .get())
        sentiment = calculate_tweet_sentiment(tweet.tweet_text, sentiment_dict)
        t = TweetNormalized.create(
            name=user,
            tweet_text=tweet.tweet_text,
            country=country,
            display_url=tweet.display_url,
            lang=lang,
            created_at=tweet.created_at,
            location=tweet.location,
            tweet_sentiment=sentiment)
        t.save()
        counter -= 1
        message = 'Tweet sentiment calculated, {} units remaining'
        print(message.format(counter))


def print_results():
    country = (Country
        .select()
        .join(TweetNormalized)
        .where(Country.id == TweetNormalized.country))
    user = (User
        .select()
        .join(TweetNormalized)
        .where(User.id == TweetNormalized.name))

    happiest_country = country.order_by(
        -TweetNormalized.tweet_sentiment).get().country_code
    happiest_user = user.order_by(-TweetNormalized.tweet_sentiment).get().name
    happiest_location = user.order_by(
        -TweetNormalized.tweet_sentiment).get().location

    unhappiest_country = country.order_by(
        TweetNormalized.tweet_sentiment).get().country_code
    unhappiest_user = user.order_by(TweetNormalized.tweet_sentiment).get().name
    unhappiest_location = user.order_by(
        TweetNormalized.tweet_sentiment).get().location

    print()
    print('Happiest country is: {}'.format(happiest_country))
    print('Happiest user is: {}'.format(happiest_user))
    print('Happiest location is: {}'.format(happiest_location))
    print()
    print('Unhappiest country is: {}'.format(unhappiest_country))
    print('Unhappiest user is: {}'.format(unhappiest_user))
    print('Unhappiest location is: {}'.format(unhappiest_location))

if __name__ == '__main__':

    db.connect()
    db.create_tables([TweetInitial, TweetNormalized, Language, Country, User])
    fill_tweet_table()
    fill_user_table()
    fill_country_table()
    fill_language_table()
    calculate_tweets_sentiment()
    print_results()
    db.close()
