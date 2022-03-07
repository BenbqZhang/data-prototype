from dash import Dash, html, dcc, Input, Output
import plotly.express as px

import math
from data import realdata

app = Dash(__name__)

whole_df = realdata.load_whole_loc1()
page_capacity = int(5*60*1000 / 10) # five minutes data per page
line_num = len(whole_df.index)
page_num = math.ceil(line_num/page_capacity)
current_page = 0

range_left, range_right = 0, 0
annote_left, annote_right = 0, 0

GROUND_LABELS=['normal', 'snow', 'ice']
label_colors = {
        'normal' : 'blue',
        'snow' : 'red',
        'ice' : 'green'
}
current_label = ''
annotated_labels = []

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
        dcc.Dropdown(id='annotation-dropdown', options=GROUND_LABELS),
        html.Button(id='left-btn', children='left'),
        html.Button(id='right-btn', children='right'),
        html.Button(id='submit-btn', children='submit'),
    ]),
    dcc.Graph(id="loc1-graph"),
    html.P(id='current-range'),
    html.Div(id='hidden-div', style={'display' : 'none'}),
    dcc.Slider(1, page_num, 1, value=1, id='page-slider'),
])

def save_labels(file, labels):
    labels_str = ','.join([str(lbl) for lbl in labels])
    with open(file, 'a') as f:
        f.write(labels_str + '\n')

@app.callback(
        Output('current-range', 'children'),
        Input('loc1-graph', 'relayoutData'),
)
def update_range(relayoutData):
    global range_left, range_right
    if relayoutData and 'xaxis.range[0]' in relayoutData:
        range_left, range_right = relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']
    return f'{range_left}, {range_right}'

@app.callback(
        Output('hidden-div', 'children'),
        Input('annotation-dropdown', 'value')
)
def update_current_label(value):
    global current_label
    if value is not None:
        current_label = value
    return ''

left_clicks_old, right_clicks_old, submit_clicks_old = 0, 0, 0
fig_backup = create_figure(whole_df[0:page_capacity])

@app.callback(
        Output('loc1-graph', 'figure'),
        Input('left-btn', 'n_clicks'),
        Input('right-btn', 'n_clicks'),
        Input('submit-btn', 'n_clicks'),
        Input('page-slider', 'value'),
)
def update_annote(left_clicks, right_clicks, submit_clicks, slider_value):
    global annote_left, annote_right
    global left_clicks_old, right_clicks_old, submit_clicks_old, current_page
    global fig_backup
    fig = fig_backup

    if slider_value != current_page:
        current_page = slider_value
        start = (current_page - 1) * page_capacity
        end= current_page * page_capacity
        df = whole_df[start:end]
        fig = create_figure(df)

    if left_clicks and left_clicks > 0 and left_clicks != left_clicks_old:
        annote_left = range_left
        lcolor = label_colors[current_label] if current_label in label_colors else 'black'
        fig.add_vline(x=annote_left, line_width=3, line_dash='dash',
                line_color=lcolor)
        fig.update_xaxes(range=[range_left, range_right])
        left_clicks_old = left_clicks

    if right_clicks and right_clicks > 0 and right_clicks != right_clicks_old:
        annote_right = range_right
        lcolor = label_colors[current_label] if current_label in label_colors else 'black'
        fig.add_vline(x=annote_right, line_width=3, line_dash='dash',
                line_color=lcolor)
        fig.update_xaxes(range=[range_left, range_right])
        right_clicks_old = right_clicks

    if submit_clicks and submit_clicks > 0 and submit_clicks != submit_clicks_old:
        annotated_labels.append((annote_left, annote_right, current_label))
        save_labels('dataset/processed_data/annotation_result/loc1_realdata_anno.txt', annotated_labels[-1])
        fcolor = label_colors[current_label] if current_label in label_colors else 'black'
        fig.add_vrect(x0=annote_left, x1=annote_right,
                annotation_text=current_label, annotation_position='top left',
                fillcolor=fcolor, opacity=0.25, line_width=0)
        fig.update_xaxes(range=[range_left, range_right])
        submit_clicks_old = submit_clicks

    fig_backup = fig

    return fig

