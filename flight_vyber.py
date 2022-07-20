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
import panel.widgets as pnw

from flight_utils_vyber import get_flights, filter_flights, get_extent, eu_airlines

pn.extension()

# %%
# FLIGHT TRACKING
x_range, y_range, ratio = get_extent()

# init flight data
f_df = get_flights()
global flight_source

flight_source = ColumnDataSource(filter_flights(f_df))
airline_vyber = pnw.RadioButtonGroup(options=eu_airlines, value="AllAir", width=150, height=200, orientation='vertical')


def update():
    # update flight data
    f_df = get_flights()
    flight_source.data = filter_flights(f_df,airline_vyber.value)
    pn.io.push_notebook(appka)

pn.state.add_periodic_callback(update, 10500);  # 6000 ms for authenticated user

# %%
WIDTH = 900
x_range, y_range, ratio = get_extent()


@pn.depends(airline_vyber)
def view(airline_vyber):
    global flight_source
    p = figure(x_range=x_range, y_range=y_range, x_axis_type='mercator', y_axis_type='mercator',
               plot_width=WIDTH, plot_height=int(WIDTH * ratio))
    tile_prov = get_provider(STAMEN_TERRAIN)
    p.add_tile(tile_prov, level='image')
    flight_source = ColumnDataSource(filter_flights(f_df,vyber=airline_vyber))

    # diamond, rotated by rot_angle
    p.diamond('x', 'y', source=flight_source, fill_color='green', hover_color='yellow', size=10, fill_alpha=0.6, line_width=0,
              angle_units='deg', angle='rot_angle')

    my_hover = HoverTool()
    my_hover.tooltips = [('Airline', '@airline'), ('Origin Country', '@origin_country'),
                         ('velocity(m/s)', '@velocity'), ('Altitude(m)', '@baro_altitude{00000}')]

    p.add_tools(my_hover)
    return pn.panel(p)

curdoc().title = 'REAL TIME FLIGHT TRACKING'

# %%
# only for notebook
appka = pn.Row(airline_vyber, view).servable()

# %%
# appka

