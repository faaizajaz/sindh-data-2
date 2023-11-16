import json
from collections import deque

import geopandas as gpd
import pandas as pd
import plotly.express as px
from dash import callback, dcc, html
from dash.dcc.Store import Store
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from utils.settings import MAPBOX_TOKEN
from werkzeug import datastructures


def serve_sidebar():
    return html.Div(
        id="sidebar",
        children=[
            dcc.Store(id="selected-parameters-memory"),
            html.H5("Select data"),
            dcc.Checklist(
                id="data-selection",
                options=["SFERP Infra", "SFERP Livelihood", "Dispensaries", "Schools"],
            ),
            html.Div(id="test-data"),
        ],
    )


@callback(
    Output("main-map", "figure", allow_duplicate=True),
    Output("selected-parameters-memory", "data"),
    Input("selected-districts-df", "data"),
    Input("data-selection", "value"),
    prevent_initial_call=True,
)
def sidebar_data_update(selected_districts_df, data_selection):
    if selected_districts_df is None:
        raise PreventUpdate
    x = pd.DataFrame.from_dict(selected_districts_df)

    x["bin_combination"] = x.apply(_calc_binary, axis=1, args=(data_selection,))

    x["bin_combination"] = x["bin_combination"].astype(str)
    x["bin_combination_parsed"] = x.apply(_parse_binary, axis=1)
    # print(data_selection)

    # print(x)
    fig = px.scatter_mapbox(
        x,
        lat=x.Latitude,
        lon=x.Longitude,
        # width=700,
        height=750,
        color=x.bin_combination_parsed,
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )

    fig.update_layout(
        mapbox_style="mapbox://styles/faaizajaz/clo2vkv5j00i801r253694dj0",
        mapbox_accesstoken=MAPBOX_TOKEN,
        margin=dict(l=30, r=30, t=30, b=30),
    )

    # print(x)
    return fig, data_selection


def _calc_binary(row, data_selection):
    bin_num = 0b0
    print(data_selection)

    if data_selection is None or len(data_selection) == 0:
        return 0b0000

    for selection in data_selection:
        if selection == "SFERP Infra":
            if row["infra_uid"] is not None:
                bin_num = bin_num + 0b1000
        if selection == "SFERP Livelihood":
            if row["scheme_uid"] is not None:
                bin_num = bin_num + 0b0100
        if selection == "Dispensaries":
            if row["disp_uid"] is not None:
                bin_num = bin_num + 0b0010
        if selection == "Schools":
            if row["school_uid"] is not None:
                bin_num = bin_num + 0b0001

    # return fixed length 4 bit number
    return f"{bin_num:04b}"


def _parse_binary(row):
    result = []

    outcomes = ["infra", "scheme", "disp", "school"]

    for i in range(len(row["bin_combination"])):
        if row["bin_combination"][i] == "1":
            result.append(outcomes[i])

    if not result:
        return None

    return " and ".join(result)
