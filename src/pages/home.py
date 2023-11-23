import json

import geopandas as gpd
import pandas as pd
import plotly.express as px
from dash import callback, dcc, html
from dash.dcc.Store import Store
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from utils.settings import MAPBOX_TOKEN

convergence_df = pd.read_csv("./src/data/convergence.csv", low_memory=False)


def serve_map():
    fig = px.scatter_mapbox(
        convergence_df,
        lat=convergence_df.Latitude,
        lon=convergence_df.Longitude,
        # width=700,
        height=850,
        custom_data=[
            convergence_df.Settlement,
            convergence_df.SMP,
            convergence_df.infra_uid,
            convergence_df.school_uid,
            convergence_df.scheme_uid,
            convergence_df.disp_uid,
            convergence_df.vill_2km_u,
        ],
        text=convergence_df["Settlement"],
    )

    fig.update_layout(
        mapbox_style="mapbox://styles/faaizajaz/clo2vkv5j00i801r253694dj0",
        mapbox_accesstoken=MAPBOX_TOKEN,
        margin=dict(l=30, r=30, t=30, b=30),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(246, 246, 246, 1)",
        ),
    )

    return html.Div(
        [
            dcc.Store(id="selected-district-memory"),
            dcc.Store(id="dispensaries-df-memory"),
            dcc.Store(id="infra-df-memory"),
            dcc.Store(id="schemes-df-memory"),
            dcc.Store(id="schools-df-memory"),
            dcc.Store(id="settlements-df-memory"),
            dcc.Store(id="selected-districts-df"),
            dcc.Dropdown(
                convergence_df.District.unique(), id="district-dropdown", multi=True
            ),
            dcc.Graph(figure=fig, id="main-map"),
        ]
    )


@callback(
    [Output("selected-district-memory", "data")],
    Input("district-dropdown", "value"),
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

    selected_districts_mask = convergence_df["District"].isin(selected_districts)

    selected_districts_df = convergence_df[selected_districts_mask]

    fig = px.scatter_mapbox(
        selected_districts_df,
        lat=selected_districts_df.Latitude,
        lon=selected_districts_df.Longitude,
        # width=700,
        height=850,
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
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(246, 246, 246, 1)",
        ),
    )

    return fig, selected_districts_df.to_dict("records")
