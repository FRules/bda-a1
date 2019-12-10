import pickle


def analyze(fans):
    with open("data_analyzing/modules/sentiment_analysis/data/sentiment_map.txt", "rb") as fp:
        statistic = pickle.load(fp)

    statistic = __remove_neutral_and_mixed_keys(statistic)
    for hashtag, match in statistic.items():
        team_home, team_away = get_team_abbreviations_by_hashtag(hashtag)
        mean_tweets = get_mean_tweets(match)
        predict_match(match, mean_tweets, fans[team_home], fans[team_away])


def get_team_abbreviations_by_hashtag(hashtag):
    return hashtag[1:4], hashtag[4:]


def predict_match(match, mean_tweets, fans_team_home, fans_team_away):
    goals_team_home, goals_team_away = 0, 0
    for minute in match.values():
        t_goals_team_home, t_goals_team_away = \
            predict_minute(minute['POSITIVE'], minute['NEGATIVE'], mean_tweets, fans_team_home, fans_team_away)
        goals_team_home = goals_team_home + t_goals_team_home
        goals_team_away = goals_team_away + t_goals_team_away
    print(goals_team_home, goals_team_away)


def predict_minute(positive_tweets, negative_tweets, mean_tweets, fans_team_home, fans_team_away):
    multiply_factor = 2
    if negative_tweets < mean_tweets * multiply_factor and positive_tweets < mean_tweets * multiply_factor:
        return 0, 0
    if negative_tweets > positive_tweets and fans_team_home > fans_team_away:
        return 0, 1
    if negative_tweets > positive_tweets and fans_team_home < fans_team_away:
        return 1, 0
    if negative_tweets < positive_tweets and fans_team_home > fans_team_away:
        return 1, 0
    if negative_tweets < positive_tweets and fans_team_home < fans_team_away:
        return 0, 1
    return 0, 0



def get_mean_tweets(match):
    amount_of_tweets = 0
    for minute in match.values():
        amount_of_tweets = amount_of_tweets + minute['POSITIVE']
        amount_of_tweets = amount_of_tweets + minute['NEGATIVE']
    return amount_of_tweets / len(match.values())

def __remove_neutral_and_mixed_keys(statistic):
    for match in statistic.values():
        for minute in match.values():
            minute.pop('NEUTRAL', None)
            minute.pop('MIXED', None)
    return statistic
