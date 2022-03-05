"""
This app demonstrates how to use rangeslider.
"""

from dash import Dash, html, dcc, Input, Output
import plotly.express as px

from data import realdata

app = Dash(__name__)

loc1_current_xaxis_start = 0
loc2_current_xaxis_start = 0

df_loc1_fivemins = realdata.load_df_loc1_fivemins_acc()
df_loc7_fivemins = realdata.load_df_loc7_fivemins_acc()


def create_figure(sensor_dataframe):
    fig = px.line(sensor_dataframe)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1s", step="second", stepmode="backward"),
                dict(count=2, label="2s", step="second", stepmode="backward"),
                dict(count=3, label="3s", step="second", stepmode="backward"),
                dict(count=5, label="5s", step="second", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig
    
app.layout = html.Div([
    html.P("sensor location 1:"),
    html.Br(),
    html.P(id="loc1-x-axis-info"),
    html.Br(),
    dcc.Graph(id="loc1-sensor-graph", figure=create_figure(df_loc1_fivemins)),

    html.P("sensor location 2:"),
    html.Br(),
    html.P(id="loc2-x-axis-info"),
    html.Br(),
    dcc.Graph(id="loc2-sensor-graph", figure=create_figure(df_loc7_fivemins)),

    html.Div(id='hidden-div', style={'display' : 'none'}),
    html.Button(id='show-btn', children='show axis info'),
])

@app.callback(
        Output('hidden-div', 'children'),
        Input('show-btn', 'n_clicks')
)
def show_info(n_clicks):
    if n_clicks and n_clicks > 0:
        with open('dataset/processed_data/sync_index.txt', 'w') as f:
            f.write(str(loc1_current_xaxis_start)+','+str(loc2_current_xaxis_start)+'\n')

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

