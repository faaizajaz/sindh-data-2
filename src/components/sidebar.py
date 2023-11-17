import json
from collections import deque

import pandas as pd
import plotly.express as px
from dash import callback, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from utils.settings import MAPBOX_TOKEN


def serve_sidebar():
    return html.Div(
        id="sidebar",
        children=[
            dcc.Store(id="selected-parameters-memory"),
            dcc.Store(id="selected-village-memory"),
            html.H5("Select data"),
            dcc.Checklist(
                id="data-selection",
                options=["SFERP Infra", "SFERP Livelihood", "Dispensaries", "Schools"],
            ),
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
    x["bin_combination_parsed"] = x.apply(_parse_binary, axis=1, args=(data_selection,))
    # print(data_selection)

    if len(data_selection) >> 1 or data_selection is None:
        fig = px.scatter_mapbox(
            x,
            lat=x.Latitude,
            lon=x.Longitude,
            # width=700,
            height=850,
            color=x.bin_combination_parsed,
            color_discrete_sequence=px.colors.qualitative.Plotly,
            custom_data=[
                x.Settlement,
                x.SMP,
                x.infra_uid,
                x.school_uid,
                x.scheme_uid,
                x.disp_uid,
                x.vill_2km_u,
            ],
            text=x["Settlement"],
        )

    else:
        fig = px.scatter_mapbox(
            x,
            lat=x.Latitude,
            lon=x.Longitude,
            # width=700,
            height=850,
            color=_return_single_data_selection(x, data_selection),
            color_discrete_sequence=px.colors.qualitative.Plotly,
            custom_data=[
                x.Settlement,
                x.SMP,
                x.infra_uid,
                x.school_uid,
                x.scheme_uid,
                x.disp_uid,
                x.vill_2km_u,
            ],
            text=x["Settlement"],
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

    # print(x)
    return fig, data_selection


@callback(
    Output("selected-village-memory", "data"),
    Input("main-map", "clickData"),
)
def handle_point_selection(selected):
    return selected


def _calc_binary(row, data_selection):
    if data_selection is None or len(data_selection) == 0:
        return ""

    data_selection_queue = deque(maxlen=len(data_selection))

    for selection in data_selection:
        if selection == "SFERP Infra":
            if row["infra_uid"] is not None:
                data_selection_queue.append("1")
            else:
                data_selection_queue.append("0")

        if selection == "SFERP Livelihood":
            if row["scheme_uid"] is not None:
                data_selection_queue.append("1")
            else:
                data_selection_queue.append("0")

        if selection == "Dispensaries":
            if row["disp_uid"] is not None:
                data_selection_queue.append("1")
            else:
                data_selection_queue.append("0")

        if selection == "Schools":
            if row["school_uid"] is not None:
                data_selection_queue.append("1")
            else:
                data_selection_queue.append("0")

    queue_string = "".join(data_selection_queue)

    return queue_string


def _parse_binary(row, data_selection):
    result = []

    outcomes = data_selection

    for i in range(len(row["bin_combination"])):
        if row["bin_combination"][i] == "1":
            result.append(outcomes[i])

    if not result:
        return None

    return " + ".join(result)


def _return_single_data_selection(df, data_selection):
    if len(data_selection) > 0:
        if data_selection[0] == "SFERP Infra":
            return df.infra_uid
        if data_selection[0] == "SFERP Livelihood":
            return df.scheme_uid
        if data_selection[0] == "Dispensaries":
            return df.disp_uid
        if data_selection[0] == "Schools":
            return df.school_uid
