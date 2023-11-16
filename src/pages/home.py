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
    # print(df2)
    # gdf = gpd.GeoDataFrame(
    #     df2,
    #     geometry=gpd.points_from_xy(df2.Longitude, df2.Latitude),
    # )

    # gdf["geometry"] = gdf.geometry.buffer(100)
    # gdf.to_file("test.shp", crs="EPSG:32642")
    # print(gdf_buffer)
    # gdf_prj = gdf.to_crs({"init": "EPSG:32642"})

    # for row in gdf.iterrows():
    #    print(row)
    # print(gdf)

    fig = px.scatter_mapbox(
        df,
        lat=df.Latitude,
        lon=df.Longitude,
        # width=700,
        height=750,
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
            dcc.Dropdown(df.District.unique(), id="district-dropdown", multi=True),
            dcc.Graph(figure=fig, id="main-map"),
            # html.Div(id="report-memory-district"),
        ]
    )


# df.insert to add a new colulmn
# then loop through using iloc
# pull out configs you want, create  a df, filter, pass to mapbox fig.

# bitshifting to keep track of spatial results
# >>> x = 0b1
# >>> x
# 1
# >>> bin(x)
# '0b1'
# >>> x = x + 0b1000
# >>> x
# 9
# >>> bin(x)
# '0b1001'

# for choosing parameter we want on the legend we can create df with binary columns accoding to selection
# then column is populated as 0b1111 for all 4 selected.
# function to build string for the legend, takes in ordered list of selected columns
# and binary number eg.g 0b0011 and builds stirng as "schools + dispensary"

#


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


# @callback(
#     [
#         Output("report-memory-district", "children"),
#         Input("selected-district-memory", "data"),
#     ]
# )
# def show_memory(selected_districts):
#     if selected_districts is None:
#         raise PreventUpdate
#     # This works
#     return selected_districts


@callback(
    Output("main-map", "figure"),
    Input("selected-district-memory", "data"),
)
def filter_selected_districts_memory(selected_districts):
    if selected_districts is None:
        raise PreventUpdate

    selected_districts_df = pd.DataFrame()
    print(selected_districts)
    # if isinstance(selected_districts, str):
    #     selected_districts_df = df[df["District"]] == str(selected_districts)
    # else:
    selected_districts_mask = df["District"].isin(selected_districts)

    selected_districts_df = df[selected_districts_mask]

    print(selected_districts_df)

    fig = px.scatter_mapbox(
        selected_districts_df,
        lat=selected_districts_df.Latitude,
        lon=selected_districts_df.Longitude,
        # width=700,
        height=750,
    )

    fig.update_layout(
        mapbox_style="mapbox://styles/faaizajaz/clo2vkv5j00i801r253694dj0",
        mapbox_accesstoken=MAPBOX_TOKEN,
        margin=dict(l=30, r=30, t=30, b=30),
    )

    return fig
