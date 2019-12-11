import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


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


def create_plot(longitudes, latitudes, cities_hashtag="all", filename="map.png"):
    plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())

    extent = [4.5, 15.5, 47.2, 56]
    ax.set_extent(extent)

    ax.coastlines(resolution='50m')
    ax.add_feature(cartopy.feature.BORDERS)
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.LAND)
    ax.add_feature(cartopy.feature.LAKES)

    ax.scatter(longitudes, latitudes, c="blue")
    cities_lats, cities_longs = create_cities_scatter_lat_long(cities_hashtag)
    ax.scatter(cities_longs, cities_lats, c="red")
    ax.title.set_text(cities_hashtag)

    plt.savefig("data_analyzing/plots/maps/" + filename)


def create_cities_scatter_lat_long(cities_hashtag="all"):
    latitudes, longitudes = [], []
    if cities_hashtag == "all":
        for key in HASHTAG_COORDINATES_MAP.values():
            latitudes.append(key["home"]["lat"])
            latitudes.append(key["away"]["lat"])
            longitudes.append(key["home"]["lng"])
            longitudes.append(key["away"]["lng"])
    else:
        latitudes.append(HASHTAG_COORDINATES_MAP[cities_hashtag]["home"]["lat"])
        latitudes.append(HASHTAG_COORDINATES_MAP[cities_hashtag]["away"]["lat"])
        longitudes.append(HASHTAG_COORDINATES_MAP[cities_hashtag]["home"]["lng"])
        longitudes.append(HASHTAG_COORDINATES_MAP[cities_hashtag]["away"]["lng"])
    return latitudes, longitudes


