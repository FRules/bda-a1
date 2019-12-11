import geopy.distance


def create_fanbase_for_all(longitudes, latitudes, hashtag_coordinates_map):
    team_fanbase_dict = get_team_fanbase_dict()
    for i in range(len(longitudes)):
        distance = 9999999999999
        found_team = None
        tweet_lng, tweet_lat = longitudes[i], latitudes[i]
        for hashtag, coordinates in hashtag_coordinates_map.items():
            for team_type, geo_data in coordinates.items():
                team_lng, team_lat = geo_data["lng"], geo_data["lat"]
                d = geopy.distance.vincenty((tweet_lat, tweet_lng), (team_lat, team_lng)).km
                if d < distance:
                    distance = d
                    if team_type == "home":
                        found_team = hashtag[1:4]
                    else:
                        found_team = hashtag[4:]
        team_fanbase_dict[found_team] = team_fanbase_dict[found_team] + 1
    print(team_fanbase_dict)
    return team_fanbase_dict


def create_fanbase_for_match(longitudes, latitudes, hashtag, hashtag_coordinates_map, team_fanbase_dict):
    for i in range(len(longitudes)):
        distance = 9999999999999
        found_team = None
        tweet_lng, tweet_lat = longitudes[i], latitudes[i]
        for h, coordinates in hashtag_coordinates_map.items():
            if hashtag != h:
                continue
            for team_type, geo_data in coordinates.items():
                team_lng, team_lat = geo_data["lng"], geo_data["lat"]
                d = geopy.distance.vincenty((tweet_lat, tweet_lng), (team_lat, team_lng)).km
                if d < distance:
                    distance = d
                    if team_type == "home":
                        found_team = hashtag[1:4]
                    else:
                        found_team = hashtag[4:]
        team_fanbase_dict[found_team] = team_fanbase_dict[found_team] + 1
    return team_fanbase_dict


def get_team_fanbase_dict():
    return {
        "BVB": 0, "BMG": 0, "FCA": 0, "FCB": 0, "SCP": 0, "SCF": 0, "SVW": 0, "BSC": 0, "FCU": 0,
        "KOE": 0, "RBL": 0, "WOB": 0, "B04": 0, "TSG": 0, "S04": 0, "M05": 0, "F95": 0, "SGE": 0
    }



