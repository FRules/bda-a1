from data_analyzing.modules.fan_prediction.geo_api import get_country_code
from data_analyzing.modules.fan_prediction.map_plot import create_plot
import data_analyzing.modules.fan_prediction.fanbase as fb

HASHTAG_COORDINATES_MAP = {
    "#BVBBMG": {"home": {"lat": 51.514244, "lng": 7.468429}, "away": {"lat": 51.18539, "lng": 6.44172}},
    "#F95M05": {"home": {"lat": 51.22172, "lng": 6.77616}, "away": {"lat": 49.98419, "lng": 8.2791}},
    "#FCAFCB": {"home": {"lat": 48.37154, "lng": 10.89851}, "away": {"lat": 48.13743, "lng": 11.57549}},
    "#FCUSCF": {"home": {"lat": 52.52437, "lng": 13.41053}, "away": {"lat": 47.9959, "lng": 7.85222}},
    "#KOESCP": {"home": {"lat": 50.941357, "lng": 6.958307}, "away": {"lat": 51.71905, "lng": 8.75439}},
    "#RBLWOB": {"home": {"lat": 51.33962, "lng": 12.37129}, "away": {"lat": 52.42452, "lng": 10.7815}},
    "#SGEB04": {"home": {"lat": 50.110924, "lng": 8.682127}, "away": {"lat": 51.0303, "lng": 6.98432}},
    "#SVWBSC": {"home": {"lat": 53.07516, "lng": 8.80777}, "away": {"lat": 52.52437, "lng": 13.41053}},
    "#TSGS04": {"home": {"lat": 49.2529, "lng": 8.87867}, "away": {"lat": 51.5075, "lng": 7.12283}}
}


def analyze(twitter_bundesliga_collection, HASHTAGS):
    latitudes, longitudes = [], []
    hashtag_latitudes_map = init_hashtag_location_map()
    hashtag_longitudes_map = init_hashtag_location_map()

    for tweet in twitter_bundesliga_collection.find():
        if tweet["geo"] is None and tweet["coordinates"] is None and tweet["place"] is None:
            continue
        country_code, lat, lng = get_country_code(tweet["geo"], tweet["coordinates"], tweet["place"])
        if country_code is None:
            continue

        match_hashtag = __return_any_match_hashtag(tweet, HASHTAGS)
        latitudes.append(lat)
        longitudes.append(lng)
        hashtag_latitudes_map[match_hashtag].append(lat)
        hashtag_longitudes_map[match_hashtag].append(lng)

    create_plot(longitudes, latitudes, HASHTAG_COORDINATES_MAP, filename="map.png")
    fb.create_fanbase_for_all(longitudes, latitudes, HASHTAG_COORDINATES_MAP)

    team_fanbase_dict = fb.get_team_fanbase_dict()

    for key in hashtag_latitudes_map.keys():
        filename = key[1:].lower()
        create_plot(hashtag_longitudes_map[key], hashtag_latitudes_map[key], HASHTAG_COORDINATES_MAP,
                    cities_hashtag=key, filename="map_" + filename + ".png")
        team_fanbase_dict = fb.create_fanbase_for_match(hashtag_longitudes_map[key], hashtag_latitudes_map[key],
                                                        key, HASHTAG_COORDINATES_MAP, team_fanbase_dict)
    print(team_fanbase_dict)
    return


def init_hashtag_location_map():
    return {'#SGEB04': [], '#RBLWOB': [], '#SVWBSC': [],
            '#F95M05': [], '#FCAFCB': [], '#FCUSCF': [],
            '#BVBBMG': [], '#KOESCP': [], '#TSGS04': []}


def __return_any_match_hashtag(tweet, HASHTAGS):
    entities = tweet["entities"]
    hashtag = search_for_hashtag(entities, HASHTAGS)
    if hashtag is not None:
        return hashtag

    if "extended_tweet" in tweet:
        if "entities" in tweet["extended_tweet"]:
            entities = tweet["extended_tweet"]["entities"]
            hashtag = search_for_hashtag(entities, HASHTAGS)
            if hashtag is not None:
                return hashtag

    if "retweeted_status" in tweet:
        if "entities" in tweet["retweeted_status"]:
            entities = tweet["retweeted_status"]["entities"]

        if "extended_tweet" in tweet["retweeted_status"]:
            if "entities" in tweet["retweeted_status"]["extended_tweet"]:
                entities = tweet["retweeted_status"]["extended_tweet"]["entities"]
        hashtag = search_for_hashtag(entities, HASHTAGS)
        if hashtag is not None:
            return hashtag

    if "quoted_status" in tweet:
        if "entities" in tweet["quoted_status"]:
            entities = tweet["quoted_status"]["entities"]

        if "extended_tweet" in tweet["quoted_status"]:
            if "entities" in tweet["quoted_status"]["extended_tweet"]:
                entities = tweet["quoted_status"]["extended_tweet"]["entities"]

        hashtag = search_for_hashtag(entities, HASHTAGS)
        if hashtag is not None:
            return hashtag

    for hashtag in HASHTAGS:
        if hashtag in tweet["text"].upper():
            return hashtag

    return None


def search_for_hashtag(entities, HASHTAGS):
    for hashtag in entities["hashtags"]:
        modified_hashtag = "#" + hashtag["text"].upper()
        if modified_hashtag in HASHTAGS:
            return modified_hashtag
