from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import data.fakedata as fakedata

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

    html.Button(id='show-annotation-btn', children='show annotation'),

    html.Div(id='hidden-div', style={'display' : 'none'}),
    html.Div(id='hidden-div-2', style={'display' : 'none'}),
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

    start, end = (slider_number-1)*fakedata.WINDOW_SIZE, slider_number*fakedata.WINDOW_SIZE
    loc1_window_df = fakedata.loc1_sensor_df[start:end]
    loc2_window_df = fakedata.loc2_sensor_df[start:end]
    return create_window_figure(loc1_window_df), create_window_figure(loc2_window_df)

@app.callback(
        Output('hidden-div', 'children'),
        Input('annotation-dropdown', 'value')
)
def update_current_window_label(label_value):
    if label_value is not None:
        annotated_labels[current_window_number] = label_value
    return ''

@app.callback(
        Output('hidden-div-2', 'children'),
        Input('show-annotation-btn', 'n_clicks')
)
def print_annotations(n_clicks):
    """
    print annotation data under stdout.
    """
    if n_clicks > 0:
        print(annotated_labels)
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
