# %%
'''
FLIGHT TRACKING WITH PYTHON AND OPEN AIR TRAFFIC DATA
by ideagora geomatics | www.geodose.com | @ideageo
'''

import requests
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.tile_providers import get_provider, STAMEN_TERRAIN
import numpy as np
from math import log, tan, pi
from bokeh.io import curdoc
import panel as pn
pn.extension()

# %%
# FUNCTION TO CONVERT GCS WGS84 TO WEB MERCATOR, DATAFRAME
def wgs84_to_web_mercator(df, lon="long", lat="lat"):
    k = 6378137
    df["x"] = df[lon] * (k * pi / 180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * pi / 360.0)) * k
    return df

# %%
#POINT
def wgs84_web_mercator_point(lon, lat):
    k = 6378137
    x = lon * k * pi / 180.0
    y = k * log(tan((90 + lat) * pi / 360.0))
    return x, y

# %%
# AREA EXTENT COORDINATE WGS84, Slovakia
lon_min, lat_min = 18, 48
lon_max, lat_max = 20, 50

# %%
# COORDINATE CONVERSION
xy_min = wgs84_web_mercator_point(lon_min, lat_min)
xy_max = wgs84_web_mercator_point(lon_max, lat_max)

# %%
# COORDINATE RANGE IN WEB MERCATOR
x_range, y_range = [xy_min[0], xy_max[0]], [xy_min[1], xy_max[1]]

# %%
# REST API QUERY URL, replace with your username and pasword on opensky-net
user_name = ''
password = ''
authdata = f'{user_name}:{password}'
base_req = f'opensky-network.org/api/states/all?lamin={lat_min}&lomin={lon_min}&lamax={lat_max}&lomax={lon_max}'
url_data = f'https://{authdata}@{base_req}' if authdata != ':' else f'https://{base_req}'

# %%
# FLIGHT TRACKING

# init bokeh column data source
flight_keys = ('icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat', 'baro_altitude', 
                'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source',
                'x', 'y', 'rot_angle', 'url')
flight_dict = {k: [] for k in flight_keys}
flight_source = ColumnDataSource(flight_dict)


def update():
    response = requests.get(url_data).json()

    # CONVERT TO PANDAS DATAFRAME
    col_names = flight_keys[:17]

    flight_df = pd.DataFrame(response['states']) 
    flight_df = flight_df.loc[:,0:16] 
    flight_df.columns = col_names
    flight_df = wgs84_to_web_mercator(flight_df)
    flight_df = flight_df.fillna('No Data')
    flight_df['rot_angle'] = -flight_df['true_track']
    icon_url = 'https://feelmath.eu/Download/airplane.png' #icon url
    flight_df['url'] = icon_url

    # UPDATE BOKEH DATASOURCE 
    flight_source.data = flight_df.to_dict(orient='list')
    pn.io.push_notebook(bk_pane)


pn.state.add_periodic_callback(update, 10500)  # can be 6000 ms for authenticated user

# PLOT AIRCRAFT POSITION
p = figure(x_range=x_range, y_range=y_range, x_axis_type='mercator', y_axis_type='mercator', 
           sizing_mode='scale_height', plot_width=900)

tile_prov = get_provider(STAMEN_TERRAIN)
p.add_tile(tile_prov, level='image')
p.image_url(url='url', x='x', y='y', source=flight_source, anchor='center', angle_units='deg', angle='rot_angle',
            h_units='screen', w_units='screen', w=40, h=40)
p.circle('x', 'y', source=flight_source, fill_color='red', hover_color='yellow', size=10, fill_alpha=0.6, line_width=0)

#ADD HOVER TOOL
my_hover = HoverTool()
my_hover.tooltips = [('Call sign', '@callsign'), ('Origin Country', '@origin_country'),
                     ('velocity(m/s)', '@velocity'), ('Altitude(m)', '@baro_altitude{00000}')]

p.add_tools(my_hover)

curdoc().title = 'REAL TIME FLIGHT TRACKING'
bk_pane = pn.panel(p).servable()

# %%
# only needed for notebook, not for panel serve ...
bk_pane
