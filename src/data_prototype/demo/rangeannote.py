from dash import Dash, html, dcc, Input, Output
import plotly.express as px

from data import fakedata

app = Dash(__name__)

df = fakedata.loc1_sensor_df

range_left, range_right = 0, 0
annote_left, annote_right = 0, 0

def create_figure(sensor_dataframe):
    fig = px.line(sensor_dataframe)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="5s", step="second", stepmode="backward"),
                dict(count=2, label="10s", step="second", stepmode="backward"),
                dict(count=3, label="15s", step="second", stepmode="backward"),
                dict(count=5, label="20s", step="second", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig

app.layout = html.Div([
    html.Div([
        html.Button(id='left-btn', children='left'),
        html.Button(id='right-btn', children='right'),
        html.Button(id='submit-btn', children='submit'),
    ]),
    dcc.Graph(id="loc1-graph"),
    html.P(id='current-range'),
])


@app.callback(
        Output('current-range', 'children'),
        Input('loc1-graph', 'relayoutData'),
)
def update_range(relayoutData):
    global range_left, range_right
    if relayoutData and 'xaxis.range[0]' in relayoutData:
        range_left, range_right = relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']
    return f'{range_left}, {range_right}'

left_clicks_old, right_clicks_old, submit_clicks_old = 0, 0, 0
fig_backup = create_figure(df)

@app.callback(
        Output('loc1-graph', 'figure'),
        Input('left-btn', 'n_clicks'),
        Input('right-btn', 'n_clicks'),
        Input('submit-btn', 'n_clicks'),
)
def update_annote(left_clicks, right_clicks, submit_clicks):
    global annote_left, annote_right
    global left_clicks_old, right_clicks_old, submit_clicks_old
    global fig_backup
    fig = fig_backup

    if left_clicks and left_clicks > 0 and left_clicks != left_clicks_old:
        annote_left = range_left
        fig.add_vline(x=annote_left, line_width=3, line_dash='dash',
                line_color='green')
        fig.update_xaxes(range=[range_left, range_right])
        left_clicks_old = left_clicks

    if right_clicks and right_clicks > 0 and right_clicks != right_clicks_old:
        annote_right = range_right
        fig.add_vline(x=annote_right, line_width=3, line_dash='dash',
                line_color='red')
        fig.update_xaxes(range=[range_left, range_right])
        right_clicks_old = right_clicks

    if submit_clicks and submit_clicks > 0 and submit_clicks != submit_clicks_old:
        print(annote_left, annote_right)
        fig.add_vrect(x0=annote_left, x1=annote_right,
                annotation_text='snow', annotation_position='top left',
                fillcolor='green', opacity=0.25, line_width=0)
        fig.update_xaxes(range=[range_left, range_right])
        submit_clicks_old = submit_clicks

    fig_backup = fig

    return fig

