import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def create_plot(longitudes, latitudes, hashtag_coordinates_map, cities_hashtag="all", filename="map.png"):
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
    cities_lats, cities_longs = create_cities_scatter_lat_long(hashtag_coordinates_map, cities_hashtag)
    ax.scatter(cities_longs, cities_lats, c="red")
    ax.title.set_text(cities_hashtag)

    plt.savefig("data_analyzing/plots/maps/" + filename)


def create_cities_scatter_lat_long(hashtag_coordinates_map, cities_hashtag="all"):
    latitudes, longitudes = [], []
    if cities_hashtag == "all":
        for key in hashtag_coordinates_map.values():
            latitudes.append(key["home"]["lat"])
            latitudes.append(key["away"]["lat"])
            longitudes.append(key["home"]["lng"])
            longitudes.append(key["away"]["lng"])
    else:
        latitudes.append(hashtag_coordinates_map[cities_hashtag]["home"]["lat"])
        latitudes.append(hashtag_coordinates_map[cities_hashtag]["away"]["lat"])
        longitudes.append(hashtag_coordinates_map[cities_hashtag]["home"]["lng"])
        longitudes.append(hashtag_coordinates_map[cities_hashtag]["away"]["lng"])
    return latitudes, longitudes


