from dash import Dash, html, Input, Output, dcc
import plotly.express as px
from collections import namedtuple

from data import realdata

app = Dash(__name__)

Sensor = namedtuple("Sensor", ["id", "title", "dataframe"])

df_loc1_fivemins = realdata.load_df_loc1_fivemins_acc()

sensor_list = [
    Sensor("sensor-no1", "sensor one", df_loc1_fivemins),
    Sensor("sensor-no2", "sensor two", df_loc1_fivemins),
    Sensor("sensor-no3", "sensor three", df_loc1_fivemins),
    Sensor("sensor-no4", "sensor five", df_loc1_fivemins),
    Sensor("sensor-no5", "sensor six", df_loc1_fivemins),
    Sensor("sensor-no6", "sensor seven", df_loc1_fivemins),
]

sensor_axis = {sensor.id: 0 for sensor in sensor_list}


def create_figure(sensor_dataframe):
    fig = px.line(sensor_dataframe)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1s", step="second", stepmode="backward"),
                    dict(count=2, label="2s", step="second", stepmode="backward"),
                    dict(count=3, label="3s", step="second", stepmode="backward"),
                    dict(count=5, label="5s", step="second", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
    )
    return fig


def generate_callback(sensor):
    @app.callback(
        Output(f"{sensor.id}-a-axis-info", "children"),
        Input(f"{sensor.id}-graph", "relayoutData"),
    )
    def update_xaxis(relayoutData):
        if relayoutData and "xaxis.range[0]" in relayoutData:
            sensor_axis[sensor.id] = relayoutData["xaxis.range[0]"]
        return f"x-axis: {str(sensor_axis[sensor.id])}"


def generate_sensors_detail(sensors):
    for sensor in sensors:
        detail_component = html.Details(
            children=[
                html.Summary(sensor.title),
                html.P(id=f"{sensor.id}-a-axis-info"),
                html.Br(),
                dcc.Graph(
                    id=f"{sensor.id}-graph", figure=create_figure(sensor.dataframe)
                ),
            ]
        )

        generate_callback(sensor)

        yield detail_component


app.layout = html.Div(
    [
        html.H1("Demo for multiple sensor graph with detials"),
        *generate_sensors_detail(sensor_list),
    ]
)
