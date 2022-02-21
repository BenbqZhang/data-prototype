"""
This app demonstrates how to synchronize different sensor channels.
"""

from dash import Dash, html, dcc, Input, Output
import plotly.express as px

from data import fakedata

app = Dash(__name__)

def create_figure(sensor_dataframe, time_index, window_size):
    """
    Create figure of fixed window-size by default.

    The point is the `range_x` argument of plotly.express.line.
    see https://plotly.com/python-api-reference/generated/plotly.express.line.html
    """
    range_start, range_end = time_index[0], time_index[window_size-1]
    return px.line(sensor_dataframe, range_x=[range_start, range_end])

app.layout = html.Div([
    html.P("sensor location 1:"),
    html.Br(),
    dcc.Graph(id="loc1-sensor-graph", figure=create_figure(fakedata.loc1_sensor_df, fakedata.loc1_date, fakedata.WINDOW_SIZE)),

    html.P("sensor location 2:"),
    html.Br(),
    dcc.Graph(id="loc2-sensor-graph", figure=create_figure(fakedata.loc2_sensor_df, fakedata.loc2_date, fakedata.WINDOW_SIZE)),
])
