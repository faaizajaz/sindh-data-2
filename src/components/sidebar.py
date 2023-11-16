import json

import geopandas as gpd
import pandas as pd
import plotly.express as px
from dash import callback, dcc, html
from dash.dcc.Store import Store
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from utils.settings import MAPBOX_TOKEN


def serve_sidebar():
    return html.Div(
        id="sidebar",
        children=[
            html.H5("Select data"),
            dcc.Checklist(
                id="data-selection",
                options=["Schools", "Dispensaries", "SFERP Infra", "SFERP Livelihood"],
            ),
            html.Div(id="test-data"),
        ],
    )


@callback(
    Output("main-map", "figure", allow_duplicate=True),
    Input("selected-districts-df", "data"),
    prevent_initial_call=True,
)
def testthis(df):
    if df is None:
        raise PreventUpdate
    x = pd.DataFrame.from_dict(df)

    x["new_bin"] = x.apply(_calc_binary, axis=1)
    x["new_bin"] = x["new_bin"].astype(str)
    print(x)
    fig = px.scatter_mapbox(
        x,
        lat=x.Latitude,
        lon=x.Longitude,
        # width=700,
        height=750,
        color=x.new_bin,
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )

    fig.update_layout(
        mapbox_style="mapbox://styles/faaizajaz/clo2vkv5j00i801r253694dj0",
        mapbox_accesstoken=MAPBOX_TOKEN,
        margin=dict(l=30, r=30, t=30, b=30),
    )

    print(x)
    return fig


def _calc_binary(row):
    bin_num = 0b0

    if row["infra_uid"] is not None:
        bin_num = bin_num + 0b1000
    if row["scheme_uid"] is not None:
        bin_num = bin_num + 0b0100
    if row["disp_uid"] is not None:
        bin_num = bin_num + 0b0010
    if row["school_uid"] is not None:
        bin_num = bin_num + 0b0001

    return bin_num
