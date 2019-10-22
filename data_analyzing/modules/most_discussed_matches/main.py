import re
from matplotlib import pyplot as plt


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
    plt.bar(range(len(distribution)), list(distribution.values()), align='center')
    plt.xticks(range(len(distribution)), list(distribution.keys()), rotation=90)
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.savefig("data_analyzing/plots/" + plot_name + ".pdf")
