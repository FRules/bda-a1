# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient
import datetime

import data_analyzing.modules.most_discussed_matches.main as most_discussed_matches
import data_analyzing.modules.tweets_during_match.main as tweets_during_match
import data_analyzing.modules.sentiment_analysis.main as sentiment_analysis
import data_analyzing.modules.score_prediction.main as score_prediction
import data_analyzing.modules.fan_prediction.main as fan_prediction

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

HIGHLIGHTS = {
              "#SGEB04": {'goals': [4, 17, 83], 'red_cards': [], 'var': [72]},
              '#RBLWOB': {'goals': [57, 85], 'red_cards': [], 'var': []},
              '#SVWBSC': {'goals': [7, 70], 'red_cards': [], 'var': []},
              '#F95M05': {'goals': [84], 'red_cards': [47], 'var': []},
              '#FCAFCB': {'goals': [1, 14, 52, 94], 'red_cards': [], 'var': []},
              '#FCUSCF': {'goals': [1, 87], 'red_cards': [], 'var': []},
              '#BVBBMG': {'goals': [61], 'red_cards': [], 'var': [35]},
              '#KOESCP': {'goals': [12, 62, 86], 'red_cards': [], 'var': [10]},
              '#TSGS04': {'goals': [73, 86], 'red_cards': [], 'var': []},
              }

FINAL_RESULTS = {"#SGEB04": {"home": 3, "away": 0},
                 "#RBLWOB": {"home": 1, "away": 1},
                 "#SVWBSC": {"home": 1, "away": 1},
                 "#F95M05": {"home": 1, "away": 0},
                 "#FCAFCB": {"home": 2, "away": 2},
                 "#FCUSCF": {"home": 2, "away": 0},
                 "#BVBBMG": {"home": 1, "away": 0},
                 "#KOESCP": {"home": 3, "away": 0},
                 "#TSGS04": {"home": 2, "away": 0}}

FANS = {"SGE": 80000, "B04": 27462, "RBL": 750, "WOB": 21500, "SVW": 39500, "BSC": 36900, "F95": 25247,
        "M05": 14200, "FCA": 17377, "FCB": 293000, "FCU": 34681, "SCF": 22000, "BVB": 154000, "BMG": 90350,
        "KOE": 101165, "SCP": 5338, "TSG": 10425, "S04": 155000}



def main():
    client = MongoClient()
    db = client.test
    twitter_bundesliga_collection = db.twitterBundesliga

    # tweets_during_match.analyze(twitter_bundesliga_collection, KICKOFFS, HIGHLIGHTS)
    # most_discussed_matches.analyze(twitter_bundesliga_collection, HASHTAGS, "most_discussed_matches")
    # sentiment_analysis.analyze(twitter_bundesliga_collection, HASHTAGS, KICKOFFS, HIGHLIGHTS,
    #                           create_analysis_file=False)
    # score_prediction.analyze(FANS)
    fan_prediction.analyze(twitter_bundesliga_collection)


if __name__ == '__main__':
    main()
