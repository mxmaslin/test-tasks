# -*- coding: utf-8 -*-
import json
import string

from peewee import *

from models import (TweetInitial,
                    TweetNormalized,
                    Language,
                    Country,
                    User,
                    db)


def fill_tweet_table():
    with open('three_minutes_tweets.json.txt') as f:
        counter = 0
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
                message = 'Tweet {} is written to tweetinitial table'
                print(message.format(counter))
    print('{} tweets written to tweetinitial table'.format(counter))


def fill_user_table():
    user_query = (TweetInitial
        .select(TweetInitial.name, TweetInitial.location))
    user_quantity = user_query.count()
    for i, user in enumerate(user_query, 1):
        User.create(
            name=user.name,
            location=user.location).save()
        message = 'Creating user {} of {} total'
        print(message.format(i, user_quantity))


def fill_country_table():
    cc_query = (TweetInitial
        .select(TweetInitial.country_code)
        .distinct())
    cc_quantity = cc_query.count()
    for i, cc in enumerate(cc_query, 1):
        Country.create(
            country_code=cc.country_code).save()
        message = 'Creating country {} of {} total'
        print(message.format(i, cc_quantity))


def fill_language_table():
    lang_query = (TweetInitial
        .select(TweetInitial.lang)
        .distinct())
    lang_quantity = lang_query.count()
    for i, lang in enumerate(lang_query, 1):
        Language.create(lang=lang.lang).save()
        message = 'Creating language {} of {} total'
        print(message.format(i, lang_quantity))


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


def calculate_tweets_sentiment(sentiment_dict):
    sentiment_dict = create_sentiment_dict()
    tweets_initial = TweetInitial.select()
    tweets_quantity = tweets_initial.count()
    for i, tweet in enumerate(tweets_initial, 1):
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
        message = 'Tweet sentiment {} of {} total calculated'
        print(message.format(i, tweets_quantity))


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


def test(sentiment_dict):
    tweet1 = '@16_Pirates any shots?'
    tweet2 = 'RT @Cancer_gk: A #Cancer may act shy and quiet, but will adamantly defend a loved one against outsiders.'
    tweet3 = '@ShivamDRao are you dumb blud.... You have missed more games than me and you are missing the most crucial bit'
    tweet4 = 'Naging malake ung uniform ko dahil sa buhol ko 😂😂'
    tweet5 = 'самый любимый вайн с лм, где они говорят: лав ю. \n я прям чувствую, что мои девочки говорят это мне'
    tweets = [tweet1, tweet2, tweet3, tweet4, tweet5]
    sentiments = list(map(
        lambda x: calculate_tweet_sentiment(x, sentiment_dict), tweets))
    assert(sentiments == [0, 1, -7, 0, 0])


if __name__ == '__main__':

    db.connect()
    db.create_tables([TweetInitial, TweetNormalized, Language, Country, User])
    fill_tweet_table()
    fill_user_table()
    fill_country_table()
    fill_language_table()
    sentiment_dict = create_sentiment_dict()
    calculate_tweets_sentiment(sentiment_dict)
    test(sentiment_dict)
    print_results()
    db.close()