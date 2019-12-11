from data_analyzing.modules.fan_prediction.geo_api import get_country_code
from data_analyzing.modules.fan_prediction.map_plot import create_plot


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

    create_plot(longitudes, latitudes, filename="map.png")
    for key in hashtag_latitudes_map.keys():
        filename = key[1:].lower()
        create_plot(hashtag_longitudes_map[key], hashtag_latitudes_map[key], cities_hashtag=key, filename="map_" + filename + ".png")
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
