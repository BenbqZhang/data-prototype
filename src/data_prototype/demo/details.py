from dash import Dash, html, Input, Output

sensor_list = [
        "sensor one",
        "sensor two",
        "sensor three",
        "sensor five",
        "sensor six",
        "sensor seven"
        ]

app = Dash(__name__)

def create_detail_component(summary_name, detail_children):
    return html.Details(
            children=[
                html.Summary(summary_name),
                detail_children
                ]
            )

def generate_detail_list(alist):
    for name in alist:
        detail_children = html.Div([
            html.H2(f"{name}'s Title"),
            html.Hr(),
            html.P(f"{name}'s content")
            ])
        yield create_detail_component(name, detail_children)

app.layout = html.Div([
    html.H1("Demo for details"),
    *generate_detail_list(sensor_list)
    ])

