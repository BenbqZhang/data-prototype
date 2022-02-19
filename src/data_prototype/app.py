from dash import Dash, html, dcc, Input, Output
import plotly.express as px

import numpy as np
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Dash App for Time-series-data Annotation', id='app-title', style={'textAlign':'center'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
