import os

import dash
import dash_bootstrap_components as dbc
from dash import html
from flask import Flask
from utils.settings import APP_DEBUG, APP_HOST, MAPBOX_TOKEN

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
    return html.Div("Bootstrapped")


app.layout = serve_layout
server = app.server

if __name__ == "__main__":
    app.run_server(host=APP_HOST, port=8085, debug=APP_DEBUG)
