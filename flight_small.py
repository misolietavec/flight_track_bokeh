# %%
'''
FLIGHT TRACKING WITH PYTHON AND OPEN AIR TRAFFIC DATA
by ideagora geomatics | www.geodose.com | @ideageo
'''

from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.tile_providers import get_provider, STAMEN_TERRAIN
from bokeh.io import curdoc
import panel as pn
from flight_utils import get_flights_df, get_extent

pn.extension()

# %%
# FLIGHT TRACKING
x_range, y_range = get_extent()

# init bokeh column data source
rel_df = get_flights_df("mikeslov", "notbkk12")
flight_dict = rel_df.to_dict(orient='list')
flight_source = ColumnDataSource(flight_dict)


def update():
    # UPDATE BOKEH DATASOURCE 
    rel_df = get_flights_df("mikeslov", "notbkk12")
    flight_source.data = rel_df.to_dict(orient='list')


pn.state.add_periodic_callback(update, 6000)  # 6000 ms

p = figure(x_range=x_range, y_range=y_range, x_axis_type='mercator', y_axis_type='mercator',
           sizing_mode='scale_height', plot_width=900)

tile_prov = get_provider(STAMEN_TERRAIN)
p.add_tile(tile_prov, level='image')
p.image_url(url='url', x='x', y='y', source=flight_source, anchor='center', angle_units='deg', angle='rot_angle',
            h_units='screen', w_units='screen', w=40, h=40)
p.circle('x', 'y', source=flight_source, fill_color='red', hover_color='yellow', size=10, fill_alpha=0.6, line_width=0)

my_hover = HoverTool()
my_hover.tooltips = [('Call sign', '@callsign'), ('Origin Country', '@origin_country'),
                     ('velocity(m/s)', '@velocity'), ('Altitude(m)', '@baro_altitude{00000}')]

p.add_tools(my_hover)

curdoc().title = 'REAL TIME FLIGHT TRACKING'
pn.panel(p).servable()
