from urllib.request import Request, urlopen
import json


def get_country_code(geo, coordinates, place):
    lat, lng = -1, -1
    if geo is not None:
        lat, lng = geo["coordinates"][0], geo["coordinates"][1]
    elif coordinates is not None:
        lat, lng = coordinates["coordinates"][1], coordinates["coordinates"][0]
    elif place is not None:
        if "bounding_box" in place and "coordinates" in place["bounding_box"] and \
                place["bounding_box"]["coordinates"] is not None:
            lat, lng = place["bounding_box"]["coordinates"][0][0][1], place["bounding_box"]["coordinates"][0][0][0]

    if lat == -1 and lng == -1:
        print("No coordinates in tweet found")
        return None

    result = call_api(lat, lng)
    if result["error"] is None:
        return result["code"], lat, lng

    print(result["error"])
    return None


def call_api(lat, lng):
    url = 'http://localhost:3000/countryCode?lat=' + str(lat) + '&lng=' + str(lng)
    req = Request(url)
    return json.load(urlopen(req))
