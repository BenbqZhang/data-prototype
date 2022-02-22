"""
This app demonstrates how to synchronize different sensor channels.
"""

from dash import Dash, html, dcc, Input, Output
import plotly.express as px

from data import fakedata

app = Dash(__name__)

loc1_current_xaxis_start = 0
loc2_current_xaxis_start = 0

def create_figure(sensor_dataframe, time_index, window_size):
    """
    Create figure of fixed window-size by default.

    The point is the `range_x` argument of plotly.express.line.
    see https://plotly.com/python-api-reference/generated/plotly.express.line.html
    """
    range_start, range_end = time_index[0], time_index[window_size-1]
    fig = px.line(sensor_dataframe, range_x=[range_start, range_end])
    fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
    return fig

app.layout = html.Div([
    html.P("sensor location 1:"),
    html.Br(),
    html.P(id="loc1-x-axis-info"),
    html.Br(),
    dcc.Graph(id="loc1-sensor-graph", figure=create_figure(fakedata.loc1_sensor_df, fakedata.loc1_date, fakedata.WINDOW_SIZE)),

    html.P("sensor location 2:"),
    html.Br(),
    html.P(id="loc2-x-axis-info"),
    html.Br(),
    dcc.Graph(id="loc2-sensor-graph", figure=create_figure(fakedata.loc2_sensor_df, fakedata.loc2_date, fakedata.WINDOW_SIZE)),

    html.Div(id='hidden-div', style={'display' : 'none'}),
    html.Button(id='show-btn', children='show axis info'),
])

@app.callback(
        Output('hidden-div', 'children'),
        Input('show-btn', 'n_clicks')
)
def show_info(n_clicks):
    if n_clicks and n_clicks > 0:
        print(loc1_current_xaxis_start, loc2_current_xaxis_start)

@app.callback(
        Output('loc1-x-axis-info', 'children'),
        Input('loc1-sensor-graph', 'relayoutData')
)
def update_loc1_xaxis(relayoutData):
    global loc1_current_xaxis_start
    if relayoutData and 'xaxis.range[0]' in relayoutData:
        loc1_current_xaxis_start = relayoutData['xaxis.range[0]']
    return str(loc1_current_xaxis_start)

@app.callback(
        Output('loc2-x-axis-info', 'children'),
        Input('loc2-sensor-graph', 'relayoutData')
)
def update_loc2_xaxis(relayoutData):
    global loc2_current_xaxis_start
    if relayoutData and 'xaxis.range[0]' in relayoutData:
        loc2_current_xaxis_start = relayoutData['xaxis.range[0]']
    return str(loc2_current_xaxis_start)

