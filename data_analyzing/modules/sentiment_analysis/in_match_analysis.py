from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import pickle


DURATION_FIRST_HALF = 45
DURATION_HALF_TIME = 17
DURATION_SECOND_HALF = 50  # extended time + buffer


def analyze(analysis_data: list, hashtags: list, kickoff: list, highlights: list):
    # statistic will hold a distribution on how the
    # sentiment data is distributed through the matches
    # for each minute.
    # It will look like:
    # {
    #   "#FCAFCB": {
    #       1: {
    #           "POSITIVE": 800,
    #           "NEGATIVE": 100,
    #           "NEUTRAL": 1600,
    #           "MIXED": 0
    #       },
    #       2: {
    #           "POSITIVE": 10,
    #           "NEGATIVE": 20,
    #           "NEUTRAL": 40,
    #           "MIXED": 0
    #       },
    #       ...
    #   },
    #   ...
    # }
    statistic = __init_statistic_dict(hashtags)
    for entry in analysis_data:
        match_hashtag = __get_match_hashtag(entry, hashtags)
        kickoff_timestamp = get_timestamp_of_kickoff(kickoff[match_hashtag])
        half_time_start_timestamp = get_timestamp_of_half_time_start(kickoff[match_hashtag])
        half_time_end_timestamp = get_timestamp_of_half_time_end(kickoff[match_hashtag])
        final_whistle_timestamp = get_timestamp_of_final_whistle(kickoff[match_hashtag])
        sentiment = entry["Sentiment"]
        match_timestamp = int(entry["Timestamp"])
        if kickoff_timestamp < match_timestamp < half_time_start_timestamp:
            minute = __get_minute(match_timestamp, kickoff[match_hashtag], first_half=True)
        elif half_time_end_timestamp < match_timestamp < final_whistle_timestamp:
            minute = __get_minute(match_timestamp, kickoff[match_hashtag], first_half=False)
        else:
            continue
        statistic[match_hashtag][minute][sentiment] += 1

    __plot_results(statistic, "in_match")
    __plot_results(statistic, "neutral_in_match", include_neutral=True)
    __save_statistic(statistic)


def __save_statistic(statistic):
    with open("data_analyzing/modules/sentiment_analysis/data/sentiment_map.txt", "wb") as fp:
        pickle.dump(statistic, fp)


def __plot_results(distribution, plot_name, include_neutral=False):
    for match_hashtag, minute_data in list(distribution.items()):
        match_withouth_hashtag = match_hashtag[1:]

        x = np.arange(len(list(distribution[match_hashtag].keys())))
        positive = __get_number_of_tweets_by_sentiment(minute_data, "POSITIVE")
        negative = __get_number_of_tweets_by_sentiment(minute_data, "NEGATIVE")
        neutral = __get_number_of_tweets_by_sentiment(minute_data, "NEUTRAL")

        fig, ax = plt.subplots()

        if include_neutral:
            width = 0.2
            rectangle_1 = ax.bar(x - width, positive, width, color='g', label='Positive')
            rectangle_2 = ax.bar(x, negative, width, color='r', label='Negative')
            rectangle_3 = ax.bar(x + width, neutral, width, color='b', label='Neutral')
        else:
            width = 0.35
            rectangle_1 = ax.bar(x - width / 2, positive, width, color='g', label='Positive')
            rectangle_2 = ax.bar(x + width / 2, negative, width, color='r', label='Negative')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Number of tweets')
        ax.set_title('Sentiment analysis of tweets of match ' + match_hashtag)
        ax.set_xticks(x)
        ax.set_xticklabels(list(distribution[match_hashtag].keys()))
        ax.legend()

        i = 0
        for label in ax.get_xaxis().get_ticklabels():
            i += 1
            if i % 5 != 1:
                label.set_visible(False)

        # auto_label(ax, rectangle_1)
        # auto_label(ax, rectangle_2)

        plt.gcf().subplots_adjust(bottom=0.25)
        plt.savefig("data_analyzing/plots/sentiment_analysis/in_match/" + plot_name + "_" + match_withouth_hashtag + ".pdf")


def __get_number_of_tweets_by_sentiment(minute_data, sentiment):
    bar = []
    for minute in list(minute_data.values()):
        bar.append(minute[sentiment])
    return bar


def __init_statistic_dict(hashtags: list) -> dict:
    statistic = {}
    for hashtag in hashtags:
        statistic[hashtag] = {}
        minutes = {minute: {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0, "MIXED": 0} for minute in range(95)}
        statistic[hashtag] = minutes
    return statistic


def __get_match_hashtag(entry_in_analysis_data: dict, hashtags: list):
    for hashtag in entry_in_analysis_data["Hashtags"]:
        if hashtag in hashtags:
            return hashtag


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


def __get_minute(match_timestamp: int, kickoff: datetime, first_half: bool) -> int:
    tweet_created_date_time = datetime.fromtimestamp(match_timestamp / 1000)
    if first_half:
        return int(((tweet_created_date_time - kickoff).seconds / 60))
    else:
        return int(((tweet_created_date_time - kickoff).seconds / 60) - DURATION_HALF_TIME)
