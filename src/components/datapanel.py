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


def serve_datapanel():
    return html.Div(
        id="datapanel",
        children=[
            html.H5("SFERP Infrastructure"),
            dash_table.DataTable(
                # data=EDUCATION_DATA.to_dict(orient="records"),
                # columns=[{"name": i, "id": i} for i in EDUCATION_DATA.columns],
                id="infra-table",
                page_current=0,
                page_size=5,
                style_table={"overflowX": "auto"},
            ),
            html.H5("SELECT Schools"),
            dash_table.DataTable(
                # data=EDUCATION_DATA.to_dict(orient="records"),
                # columns=[{"name": i, "id": i} for i in EDUCATION_DATA.columns],
                id="schools-table",
                page_current=0,
                page_size=5,
                style_table={"overflowX": "auto"},
            ),
            html.H5("SFERP Schemes"),
            dash_table.DataTable(
                # data=EDUCATION_DATA.to_dict(orient="records"),
                # columns=[{"name": i, "id": i} for i in EDUCATION_DATA.columns],
                id="schemes-table",
                page_current=0,
                page_size=5,
                style_table={"overflowX": "auto"},
            ),
            html.H5("SHP Dispensaries"),
            dash_table.DataTable(
                # data=EDUCATION_DATA.to_dict(orient="records"),
                # columns=[{"name": i, "id": i} for i in EDUCATION_DATA.columns],
                id="disp-table",
                page_current=0,
                page_size=5,
                style_table={"overflowX": "auto"},
            ),
            html.H5("Villages in 2km"),
            dash_table.DataTable(
                # data=EDUCATION_DATA.to_dict(orient="records"),
                # columns=[{"name": i, "id": i} for i in EDUCATION_DATA.columns],
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
    # selected_districts_df = pd.DataFrame.from_dict(df)
    selected_village_data = village["points"][0]["customdata"]
    # print(selected_village_data)
    village_name = selected_village_data[0]
    village_smp = selected_village_data[1]
    village_infra = _parse_uid_group(selected_village_data[2])
    village_schools = _parse_uid_group(selected_village_data[3])
    village_schemes = _parse_uid_group(selected_village_data[4])
    village_disp = _parse_uid_group(selected_village_data[5])
    village_2km_vill = _parse_uid_group(selected_village_data[6])

    settlements_df["UID"] = settlements_df["UID"].astype(str)
    # 2k_vill_df = _find_in_df(settlements_df, village_2km_vill, "UID")
    near_vill_df = _find_in_df(settlements_df, village_2km_vill, "UID")

    infra_df["UID"] = infra_df["UID"].astype(str)
    near_infra_df = _find_in_df(infra_df, village_infra, "UID")

    schemes_df["UID"] = schemes_df["UID"].astype(str)
    near_schemes_df = _find_in_df(schemes_df, village_schemes, "UID")

    schools_df["UID"] = schools_df["UID"].astype(str)
    near_schools_df = _find_in_df(schools_df, village_schools, "UID")

    dispensaries_df["S_No"] = dispensaries_df["S_No"].astype(str)
    near_disp_df = _find_in_df(dispensaries_df, village_disp, "S_No")

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
    print(find_list)
    df2 = df[df[column_name].isin(find_list)]
    return df2
