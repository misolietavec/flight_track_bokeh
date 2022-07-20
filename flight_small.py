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
from flight_utils import get_flights, get_extent

pn.extension()

# %%
# FLIGHT TRACKING
x_range, y_range, ratio = get_extent()

# init bokeh column data source
flight_source = ColumnDataSource(get_flights(as_DF=False))


def update():
    # UPDATE BOKEH DATASOURCE
    flight_source.data = get_flights(as_DF=False)
    pn.io.push_notebook(bk_pane)


pn.state.add_periodic_callback(update, 10500);  # 6000 ms for authenticated user

# %%
# DISPLAY ON MAP
WIDTH = 900
p = figure(x_range=x_range, y_range=y_range, x_axis_type='mercator', y_axis_type='mercator', 
           plot_width=WIDTH, plot_height = int(WIDTH * ratio))

tile_prov = get_provider(STAMEN_TERRAIN)
p.add_tile(tile_prov, level='image')

# triangle, rotated by rot_angle
p.circle('x', 'y', source=flight_source, fill_color='red', hover_color='yellow', size=10, fill_alpha=0.6, line_width=0)

my_hover = HoverTool()
my_hover.tooltips = [('Airline', '@airline'), ('Origin Country', '@origin_country'),
                     ('velocity(m/s)', '@velocity'), ('Altitude(m)', '@baro_altitude{00000}')]

p.add_tools(my_hover)

curdoc().title = 'REAL TIME FLIGHT TRACKING'

bk_pane = pn.panel(p).servable()

# %%
# only for notebook
bk_pane
