import os

import dash
import dash_bootstrap_components as dbc
import geopandas
import pandas as pd
import plotly.express as px
from dash import html
from flask import Flask
from pages.home import serve_map
from utils.settings import APP_DEBUG, APP_HOST, APP_PORT, MAPBOX_TOKEN

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    # Check if a device is mobile
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True,
    title="Sindh Settlements Explorer",
)


def serve_layout():
    return dbc.Container(
        [
            dbc.Row(
                [
                    # Left Sidebar
                    dbc.Col(
                        html.Div("Sidebar"),
                        width=2,
                    ),
                    # Main content
                    dbc.Col(
                        children=[serve_map()],
                        width=10,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


app.layout = serve_layout
server = app.server

if __name__ == "__main__":
    app.run_server(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
