import json
from collections import deque

import pandas as pd
import plotly.express as px
from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from utils.settings import MAPBOX_TOKEN

dispensaries_df = pd.read_csv("./src/data/dispensaries.csv", low_memory=False)
infra_df = pd.read_csv("./src/data/infra-data.csv", low_memory=False)
schemes_df = pd.read_csv("./src/data/schemes-data.csv", low_memory=False)
schools_df = pd.read_csv("./src/data/schools-data.csv", low_memory=False)
settlements_df = pd.read_csv("./src/data/convergence.csv", low_memory=False)

settlements_df["UID"] = settlements_df["UID"].astype(str)
infra_df["UID"] = infra_df["UID"].astype(str)
schemes_df["UID"] = schemes_df["UID"].astype(str)
schools_df["UID"] = schools_df["UID"].astype(str)
dispensaries_df["S_No"] = dispensaries_df["S_No"].astype(str)


def serve_datapanel():
    return html.Div(
        id="datapanel",
        children=[
            html.H5("SFERP Infrastructure"),
            dash_table.DataTable(
                id="infra-table",
                page_current=0,
                page_size=5,
                style_table={"overflowX": "auto"},
            ),
            html.H5("SELECT Schools"),
            dash_table.DataTable(
                id="schools-table",
                page_current=0,
                page_size=5,
                style_table={"overflowX": "auto"},
            ),
            html.H5("SFERP Schemes"),
            dash_table.DataTable(
                id="schemes-table",
                page_current=0,
                page_size=5,
                style_table={"overflowX": "auto"},
            ),
            html.H5("SHP Dispensaries"),
            dash_table.DataTable(
                id="disp-table",
                page_current=0,
                page_size=5,
                style_table={"overflowX": "auto"},
            ),
            html.H5("Villages in 2km"),
            dash_table.DataTable(
                id="vill-table",
                page_current=0,
                page_size=5,
                style_table={"overflowX": "auto"},
            ),
        ],
    )


@callback(
    Output("infra-table", "data"),
    Output("schools-table", "data"),
    Output("schemes-table", "data"),
    Output("disp-table", "data"),
    Output("vill-table", "data"),
    Input("selected-village-memory", "data"),
    Input("selected-districts-df", "data"),
)
def populate_datapanel(village, df):
    selected_village_data = village["points"][0]["customdata"]

    village_name = selected_village_data[0]
    village_smp = selected_village_data[1]

    near_vill_df = _find_in_df(
        settlements_df, _parse_uid_group(selected_village_data[6]), "UID"
    )

    near_infra_df = _find_in_df(
        infra_df, _parse_uid_group(selected_village_data[2]), "UID"
    )

    near_schemes_df = _find_in_df(
        schemes_df, _parse_uid_group(selected_village_data[4]), "UID"
    )

    near_schools_df = _find_in_df(
        schools_df, _parse_uid_group(selected_village_data[3]), "UID"
    )

    near_disp_df = _find_in_df(
        dispensaries_df, _parse_uid_group(selected_village_data[5]), "S_No"
    )

    return (
        near_infra_df.to_dict("records"),
        near_schools_df.to_dict("records"),
        near_schemes_df.to_dict("records"),
        near_disp_df.to_dict("records"),
        near_vill_df.to_dict("records"),
    )


# Settlement | SMP | infra_uid | school_uid | scheme_uid | disp_uid | vill_2km_u
def _parse_uid_group(uid_group):
    if uid_group is not None:
        separated_group = uid_group.split("-")
        return separated_group
    else:
        return []


def _find_in_df(df, find_list, column_name):
    df2 = df[df[column_name].isin(find_list)]
    return df2
