from dash import Dash, html, dcc
import plotly.express as px

from data import realdata

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=px.line(realdata.load_df_range_1_2())),
])
