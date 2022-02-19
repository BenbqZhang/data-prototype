from dash import Dash, html, dcc, Input, Output
import plotly.express as px

import numpy as np
import pandas as pd
import random

random.seed(45)
# fake data to simulate collected real data
LOC1_SAMPLE_NUM = int(1e4)
LOC2_SAMPLE_NUM = int(1e4)+random.randint(100, 1000)
COLUMNS = ['acc_' + channel for channel in ['x', 'y', 'z']]

loc1_date = pd.date_range(start='2020-12-28 14:53:43.435', periods=LOC1_SAMPLE_NUM, freq='10ms')
loc2_date = pd.date_range(start='2020-12-28 14:53:43.435', periods=LOC2_SAMPLE_NUM, freq='10ms')
loc1_sensor_df = pd.DataFrame(np.random.randn(LOC1_SAMPLE_NUM, len(COLUMNS)), index=loc1_date, columns=COLUMNS)
loc2_sensor_df = pd.DataFrame(np.random.randn(LOC2_SAMPLE_NUM, len(COLUMNS)), index=loc2_date, columns=COLUMNS)

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Dash App for Time-series-data Annotation', id='app-title', style={'textAlign':'center'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
