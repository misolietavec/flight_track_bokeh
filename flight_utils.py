# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import requests
import numpy as np
from math import log, tan, pi

# %%
slovensko = [48,50,18,21]  # pridat ine, okolie letisk napr.
icon_url = 'https://feelmath.eu/Download/airplane.png' #icon url
flight_keys = ('icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat', 'baro_altitude', 'on_ground',
               'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source')


# %%
# FUNCTION TO CONVERT GCS WGS84 TO WEB MERCATOR, DATAFRAME
def wgs84_to_web_mercator(df, lon="long", lat="lat"):
    k = 6378137
    xlist = df[lon].values * (k * pi / 180.0)
    ylist = np.log(np.tan((90 + df[lat].values) * pi / 360.0)) * k
    return xlist, ylist


# %%
#POINT
def wgs84_web_mercator_point(lon, lat):
    k = 6378137
    x = lon * k * pi / 180.0
    y = k * log(tan((90 + lat) * pi / 360.0))
    return x, y


# %%
def get_extent(georect=slovensko):
    lat_min, lat_max, lon_min, lon_max = georect
    xy_min = wgs84_web_mercator_point(lon_min, lat_min)
    xy_max = wgs84_web_mercator_point(lon_max, lat_max)
    x_range, y_range = [xy_min[0], xy_max[0]], [xy_min[1], xy_max[1]]
    return x_range, y_range


# %%
def get_flights_states(user_name='', password='', georect=slovensko):
    authdata = f'{user_name}:{password}'
    lat_min, lat_max, lon_min, lon_max = georect
    base_req = f'opensky-network.org/api/states/all?lamin={lat_min}&lomin={lon_min}&lamax={lat_max}&lomax={lon_max}'
    url_data = f'https://{authdata}@{base_req}' if authdata != ':' else f'https://{base_req}'
    response = requests.get(url_data).json()
    return response['states']


# %%
def get_flights_df(user_name='', password='', georect=slovensko):
    states = get_flights_states(user_name, password, georect)
    df = pd.DataFrame(states)
    df.columns = flight_keys
    df_rel = df[['callsign','origin_country','baro_altitude','on_ground','velocity']].copy()
    df_rel['x'], df_rel['y'] = wgs84_to_web_mercator(df)
    df_rel['rot_angle'] = -df['true_track']
    df_rel['url'] = icon_url
    return df_rel
