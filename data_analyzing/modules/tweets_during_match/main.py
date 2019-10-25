import re
from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt


DURATION_FIRST_HALF = 45
DURATION_HALF_TIME = 17
DURATION_SECOND_HALF = 50  # extended time + buffer


def analyze(twitter_bundesliga_collection, kickoffs: dict, highlights: dict):
    for hashtag, kickoff in kickoffs.items():
        tweets_per_minute = get_tweets_per_minute(twitter_bundesliga_collection, hashtag, kickoff)
        plot_results(tweets_per_minute, hashtag[1:], highlights[hashtag])


def get_tweets_per_minute(twitter_bundesliga_collection, hashtag, kickoff: datetime):
    timestamp_kickoff = get_timestamp_of_kickoff(kickoff)
    timestamp_half_time_start = get_timestamp_of_half_time_start(kickoff)
    timestamp_half_time_end = get_timestamp_of_half_time_end(kickoff)
    timestamp_final_whistle = get_timestamp_of_final_whistle(kickoff)

    # number_before_match_tweets = get_before_match_tweets_count(twitter_bundesliga_collection, hashtag, timestamp_kickoff)
    first_half_tweets = get_first_half_tweets(twitter_bundesliga_collection, hashtag,
                                              timestamp_kickoff, timestamp_half_time_start)
    # number_half_time_tweets = get_half_time_tweets_count(twitter_bundesliga_collection, hashtag,
    #                                        timestamp_half_time_start, timestamp_half_time_end)
    second_half_tweets = get_second_half_tweets(twitter_bundesliga_collection, hashtag,
                                                timestamp_half_time_end, timestamp_final_whistle)
    # number_after_match_tweets = get_after_match_tweets_count(twitter_bundesliga_collection, hashtag, timestamp_final_whistle)

    first_half = get_tweet_distribution_for_first_half(list(first_half_tweets), kickoff)
    second_half = get_tweet_distribution_for_second_half(list(second_half_tweets), kickoff)
    merged = {**first_half, **second_half}
    return merged


def get_tweet_distribution_for_first_half(tweets, kickoff):
    minutes = {minute: 0 for minute in range(95)}
    for tweet in tweets:
        tweet_created_date_time = datetime.fromtimestamp(int(tweet["timestamp_ms"]) / 1000)
        minute = int(((tweet_created_date_time - kickoff).seconds / 60))
        if minute in minutes:
            minutes[minute] += 1
        else:
            minutes[minute] = 1
    return minutes


def get_tweet_distribution_for_second_half(tweets, kickoff):
    minutes = {}
    for tweet in tweets:
        tweet_created_date_time = datetime.fromtimestamp(int(tweet["timestamp_ms"]) / 1000)
        minute = int(((tweet_created_date_time - kickoff).seconds / 60) - DURATION_HALF_TIME)
        if minute in minutes:
            minutes[minute] += 1
        else:
            minutes[minute] = 1
    return minutes


def get_before_match_tweets_count(collection, hashtag, timestamp_kickoff):
    rgx = re.compile('.*' + hashtag + '.*', re.IGNORECASE)

    return collection.count({
        "$and": [
            {"timestamp_ms": {"$lt": str(timestamp_kickoff)}},
            {
                "$or": [
                    {"text": rgx},
                    {"retweeted_status.extended_tweet.full_text": rgx}
                ]
            }
        ]
    })


def get_first_half_tweets(collection, hashtag, timestamp_kickoff, timestamp_half_time_start):
    rgx = re.compile('.*' + hashtag + '.*', re.IGNORECASE)

    return collection.find({
        "$and": [
            {"timestamp_ms": {"$gte": str(timestamp_kickoff)}},
            {"timestamp_ms": {"$lte": str(timestamp_half_time_start)}},
            {
                "$or": [
                    {"text": rgx},
                    {"retweeted_status.extended_tweet.full_text": rgx}
                ]
            }
        ]
    })


def get_half_time_tweets_count(collection, hashtag, timestamp_half_time_start, timestamp_half_time_end):
    rgx = re.compile('.*' + hashtag + '.*', re.IGNORECASE)

    return collection.count({
        "$and": [
            {"timestamp_ms": {"$gt": str(timestamp_half_time_start)}},
            {"timestamp_ms": {"$lt": str(timestamp_half_time_end)}},
            {
                "$or": [
                    {"text": rgx},
                    {"retweeted_status.extended_tweet.full_text": rgx}
                ]
            }
        ]
    })


def get_second_half_tweets(collection, hashtag, timestamp_half_time_end, timestamp_final_whistle):
    rgx = re.compile('.*' + hashtag + '.*', re.IGNORECASE)

    return collection.find({
        "$and": [
            {"timestamp_ms": {"$gte": str(timestamp_half_time_end)}},
            {"timestamp_ms": {"$lte": str(timestamp_final_whistle)}},
            {
                "$or": [
                    {"text": rgx},
                    {"retweeted_status.extended_tweet.full_text": rgx}
                ]
            }
        ]
    })


def get_after_match_tweets_count(collection, hashtag, timestamp_final_whistle):
    rgx = re.compile('.*' + hashtag + '.*', re.IGNORECASE)

    return collection.count({
        "$and": [
            {"timestamp_ms": {"$gt": str(timestamp_final_whistle)}},
            {
                "$or": [
                    {"text": rgx},
                    {"retweeted_status.extended_tweet.full_text": rgx}
                ]
            }
        ]
    })


def get_timestamp_of_kickoff(kickoff: datetime):
    return int(datetime.timestamp(kickoff)) * 1000


def get_timestamp_of_half_time_start(kickoff: datetime):
    # we add 46. 45 minutes first half duration, 1 minute extended time
    minutes = DURATION_FIRST_HALF
    return int(datetime.timestamp(kickoff + timedelta(minutes=minutes))) * 1000


def get_timestamp_of_half_time_end(kickoff: datetime):
    # we add 62. 45 minutes first half duration, 1 minute extended time,
    # 15 minutes half time break, 1 minute buffer
    minutes = DURATION_FIRST_HALF + DURATION_HALF_TIME
    return int(datetime.timestamp(kickoff + timedelta(minutes=minutes))) * 1000


def get_timestamp_of_final_whistle(kickoff: datetime):
    # we add 115. 90 minutes match duration, 15 minutes half time,
    # 10 min for buffer and extended time
    minutes = DURATION_FIRST_HALF + DURATION_HALF_TIME + DURATION_SECOND_HALF
    return int(datetime.timestamp(kickoff + timedelta(minutes=minutes))) * 1000


def plot_results(tweets_per_minute, plot_name, highlights):
    plt.figure()
    barlist = plt.bar(range(len(tweets_per_minute)), list(tweets_per_minute.values()), align='center')
    ax = plt.gca()
    # plt.axis([0, 24, 0, 50])
    plt.xticks(range(len(tweets_per_minute)), list(tweets_per_minute.keys()), rotation=90)
    i = 0
    for goal in highlights["goals"]:
        barlist[goal].set_color("g")
    for red_card in highlights["red_cards"]:
        barlist[red_card].set_color("r")

    for label in ax.get_xaxis().get_ticklabels():
        i += 1
        if i % 5 != 1:
            label.set_visible(False)

    plt.savefig("data_analyzing/plots/tweets_during_match/" + plot_name + ".pdf")
