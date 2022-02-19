from dash import Dash, html, dcc, Input, Output
import plotly.express as px

import numpy as np
import pandas as pd
import random

random.seed(45)
WINDOW_SIZE = 128
# fake data to simulate collected real data
LOC1_SAMPLE_NUM = int(1e4)
LOC2_SAMPLE_NUM = int(1e4)+random.randint(100, 1000)
COLUMNS = ['acc_' + channel for channel in ['x', 'y', 'z']]

loc1_date = pd.date_range(start='2020-12-28 14:53:43.435', periods=LOC1_SAMPLE_NUM, freq='10ms')
loc2_date = pd.date_range(start='2020-12-28 14:53:43.435', periods=LOC2_SAMPLE_NUM, freq='10ms')
loc1_sensor_df = pd.DataFrame(np.random.randn(LOC1_SAMPLE_NUM, len(COLUMNS)), index=loc1_date, columns=COLUMNS)
loc2_sensor_df = pd.DataFrame(np.random.randn(LOC2_SAMPLE_NUM, len(COLUMNS)), index=loc2_date, columns=COLUMNS)

current_window_number = 1
GROUND_LABELS=['normal', 'snow', 'ice']
# annotation (window_number : label)
annotated_labels = {}

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Dash App for Time-series-data Annotation', id='app-title', style={'textAlign':'center'}),
    html.Hr(),

    html.Div([
        html.P('please select a label: '),
        dcc.Dropdown(id='annotation-dropdown', options=GROUND_LABELS),
    ]),

    dcc.Graph(id='loc1-sensor-graph'),
    dcc.Graph(id='loc2-sensor-graph'),
    dcc.Slider(id='slide-window-slider', min=1, max=10, step=1, value=1),

    html.Div(id='hidden-div', style={'display' : 'none'}),
])

def create_window_figure(window_df):
    return px.line(window_df)

@app.callback(
        Output('loc1-sensor-graph', 'figure'),
        Output('loc2-sensor-graph', 'figure'),
        Input('slide-window-slider', 'value')
)
def udpate_slide_window(slider_number):
    global current_window_number
    current_window_number = slider_number

    start, end = (slider_number-1)*WINDOW_SIZE, slider_number*WINDOW_SIZE
    loc1_window_df = loc1_sensor_df[start:end]
    loc2_window_df = loc2_sensor_df[start:end]
    return create_window_figure(loc1_window_df), create_window_figure(loc2_window_df)

@app.callback(
        Output('hidden-div', 'children'),
        Input('annotation-dropdown', 'value')
)
def update_current_window_label(label_value):
    annotated_labels[current_window_number] = label_value
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
