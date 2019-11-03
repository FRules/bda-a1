import re
from matplotlib import pyplot as plt
import numpy as np


def analyze(twitter_bundesliga_collection, hashtags, plot_name):
    distribution = {}
    for hashtag in hashtags:
        rgx = re.compile('.*' + hashtag + '.*', re.IGNORECASE)
        distribution[hashtag] = twitter_bundesliga_collection.count({
            "$or": [
                {"text": rgx},
                {"retweeted_status.extended_tweet.full_text": rgx}
            ]
        })

    plot_results(distribution, plot_name)


def plot_results(distribution, plot_name):
    plt.figure()

    fig, ax = plt.subplots()
    x = np.arange(len(list(distribution.keys())))

    ax.set_ylabel('Number of tweets')
    ax.set_title('Amount of tweets per match')
    ax.set_xticks(x)
    ax.set_xticklabels(list(distribution.keys()), rotation=90)

    rectangle_1 = ax.bar(x, list(distribution.values()), 0.5, label='Number of tweets')

    auto_label(ax, rectangle_1)

    plt.gcf().subplots_adjust(bottom=0.25)
    plt.savefig("data_analyzing/plots/" + plot_name + ".pdf")


def auto_label(ax, rectangles):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rectangles:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 3, height),
                    xytext=(0, 0),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
