# This file analyzes the sentiment data in general.
# That means, it will plot how people react to the matches
# in general. If you want to know, how people react pre-,
# in- and post-match, use in_match_analysis.py
import numpy as np
from matplotlib import pyplot as plt


def analyze(analysis_data: list, hashtags: list):
    # statistic will hold a distribution on how the
    # sentiment data is distributed through the matches
    # It will look like:
    # {
    #   "#FCAFCB": {
    #       "POSITIVE": 800,
    #       "NEGATIVE": 100,
    #       "NEUTRAL": 1600,
    #       "MIXED": 0
    #   },
    #   ...
    # }
    statistic = {}
    for entry in analysis_data:
        found_hashtags = __get_match_hashtags(entry, hashtags)
        sentiment = entry["Sentiment"]
        for hashtag in found_hashtags:
            if hashtag not in statistic:
                statistic[hashtag] = {
                    "POSITIVE": 0,
                    "NEGATIVE": 0,
                    "NEUTRAL": 0,
                    "MIXED": 0
                }
                statistic[hashtag][sentiment] += 1
            else:
                statistic[hashtag][sentiment] += 1
    __plot_results(statistic, "general_sentiment_analysis")
    __plot_results(statistic, "general_sentiment_analysis_neutral", include_neutral=True)


def __get_match_hashtags(entry_in_analysis_data: dict, hashtags: list):
    match_hashtags_in_entry = []
    for hashtag in entry_in_analysis_data["Hashtags"]:
        if hashtag in hashtags:
            match_hashtags_in_entry.append(hashtag)
    return match_hashtags_in_entry


def __plot_results(distribution, plot_name, include_neutral=False):
    plt.figure()

    positive = __get_number_of_tweets_by_sentiment(distribution, "POSITIVE")
    negative = __get_number_of_tweets_by_sentiment(distribution, "NEGATIVE")
    neutral = __get_number_of_tweets_by_sentiment(distribution, "NEUTRAL")
    # mixed = __get_number_of_tweets_by_sentiment(distribution, "MIXED")

    x = np.arange(len(list(distribution.keys())))

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
    ax.set_title('Sentiment analysis of tweets per match')
    ax.set_xticks(x)
    ax.set_xticklabels(list(distribution.keys()), rotation=90)
    ax.legend()

    # auto_label(ax, rectangle_1)
    # auto_label(ax, rectangle_2)

    plt.gcf().subplots_adjust(bottom=0.25)
    plt.savefig("data_analyzing/plots/sentiment_analysis/general/" + plot_name + ".pdf")


def __get_number_of_tweets_by_sentiment(distribution, sentiment):
    bar = []
    for match in list(distribution.values()):
        bar.append(match[sentiment])
    return bar


def auto_label(ax, rectangles):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rectangles:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 3, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
