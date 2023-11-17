import json

import geopandas as gpd
import pandas as pd
import plotly.express as px
from dash import callback, dcc, html
from dash.dcc.Store import Store
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from utils.settings import MAPBOX_TOKEN

df = pd.read_csv("./src/data/convergence.csv", low_memory=False)


def serve_map():
    fig = px.scatter_mapbox(
        df,
        lat=df.Latitude,
        lon=df.Longitude,
        # width=700,
        height=750,
        custom_data=[
            df.Settlement,
            df.SMP,
            df.infra_uid,
            df.school_uid,
            df.scheme_uid,
            df.disp_uid,
            df.vill_2km_u,
        ],
        text=df["Settlement"],
    )

    fig.update_layout(
        mapbox_style="mapbox://styles/faaizajaz/clo2vkv5j00i801r253694dj0",
        mapbox_accesstoken=MAPBOX_TOKEN,
        margin=dict(l=30, r=30, t=30, b=30),
        # mapbox_layers=[
        #     {
        #         "below": "traces",
        #         "color": "red",
        #         "source": json.loads(gdf.geometry.to_json()),
        #     }
        # ]
        # autosize=True,
    )

    return html.Div(
        [
            dcc.Store(id="selected-district-memory"),
            dcc.Store(id="selected-districts-df"),
            dcc.Dropdown(df.District.unique(), id="district-dropdown", multi=True),
            dcc.Graph(figure=fig, id="main-map"),
            html.Div(id="report-selected-point"),
        ]
    )


@callback(
    [Output("selected-district-memory", "data")], Input("district-dropdown", "value")
)
def set_districts_memory(selected_districts):
    if selected_districts is None:
        raise PreventUpdate
    sd = []
    for d in selected_districts:
        sd.append(d)

    return [sd]


@callback(
    Output("main-map", "figure", allow_duplicate=True),
    Output("selected-districts-df", "data"),
    Input("selected-district-memory", "data"),
    prevent_initial_call=True,
)
def filter_selected_districts_memory(selected_districts):
    if selected_districts is None:
        raise PreventUpdate

    selected_districts_df = pd.DataFrame()

    selected_districts_mask = df["District"].isin(selected_districts)

    selected_districts_df = df[selected_districts_mask]

    fig = px.scatter_mapbox(
        selected_districts_df,
        lat=selected_districts_df.Latitude,
        lon=selected_districts_df.Longitude,
        # width=700,
        height=750,
        custom_data=[
            selected_districts_df.Settlement,
            selected_districts_df.SMP,
            selected_districts_df.infra_uid,
            selected_districts_df.school_uid,
            selected_districts_df.scheme_uid,
            selected_districts_df.disp_uid,
            selected_districts_df.vill_2km_u,
        ],
        text=selected_districts_df["Settlement"],
    )

    fig.update_layout(
        mapbox_style="mapbox://styles/faaizajaz/clo2vkv5j00i801r253694dj0",
        mapbox_accesstoken=MAPBOX_TOKEN,
        margin=dict(l=30, r=30, t=30, b=30),
    )

    return fig, selected_districts_df.to_dict("records")
