# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient
import datetime

import data_analyzing.modules.most_discussed_matches.main as most_discussed_matches
import data_analyzing.modules.tweets_during_match.main as tweets_during_match
import data_analyzing.modules.sentiment_analysis.main as sentiment_analysis

HASHTAGS = ["#SGEB04", '#RBLWOB', '#SVWBSC',
            '#F95M05', '#FCAFCB', '#FCUSCF',
            '#BVBBMG', '#KOESCP', '#TSGS04']

KICKOFFS = {"#SGEB04": datetime.datetime(2019, 10, 18, 20, 30, 00, 000),
            '#RBLWOB': datetime.datetime(2019, 10, 19, 15, 30, 00, 000),
            '#SVWBSC': datetime.datetime(2019, 10, 19, 15, 30, 00, 000),
            '#F95M05': datetime.datetime(2019, 10, 19, 15, 30, 00, 000),
            '#FCAFCB': datetime.datetime(2019, 10, 19, 15, 30, 00, 000),
            '#FCUSCF': datetime.datetime(2019, 10, 19, 15, 30, 00, 000),
            '#BVBBMG': datetime.datetime(2019, 10, 19, 18, 30, 00, 000),
            '#KOESCP': datetime.datetime(2019, 10, 20, 15, 30, 00, 000),
            '#TSGS04': datetime.datetime(2019, 10, 20, 18, 00, 00, 000)}

HIGHLIGHTS = {"#SGEB04": {'goals': [4, 17, 83], 'red_cards': [], 'var': [72]},
              '#RBLWOB': {'goals': [57, 85], 'red_cards': [], 'var': []},
              '#SVWBSC': {'goals': [7, 70], 'red_cards': [], 'var': []},
              '#F95M05': {'goals': [84], 'red_cards': [47], 'var': []},
              '#FCAFCB': {'goals': [1, 14, 52, 94], 'red_cards': [], 'var': []},
              '#FCUSCF': {'goals': [1, 87], 'red_cards': [], 'var': []},
              '#BVBBMG': {'goals': [61], 'red_cards': [], 'var': [35]},
              '#KOESCP': {'goals': [12, 62, 86], 'red_cards': [], 'var': [10]},
              '#TSGS04': {'goals': [73, 86], 'red_cards': [], 'var': []},
              }


def main():
    client = MongoClient()
    db = client.test
    twitter_bundesliga_collection = db.twitterBundesliga

    # tweets_during_match.analyze(twitter_bundesliga_collection, KICKOFFS, HIGHLIGHTS)
    # most_discussed_matches.analyze(twitter_bundesliga_collection, HASHTAGS, "most_discussed_matches")
    sentiment_analysis.analyze(twitter_bundesliga_collection, HASHTAGS, KICKOFFS, HIGHLIGHTS,
                               create_analysis_file=False)


if __name__ == '__main__':
    main()
