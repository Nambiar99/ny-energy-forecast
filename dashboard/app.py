import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
import dash

from components.bars import sidebar, titlebar
from utils.callbacks import register_app_callbacks

import os
from dotenv import load_dotenv
load_dotenv()

app = Dash(
	__name__,
	use_pages=True,
	external_stylesheets=[dbc.themes.BOOTSTRAP],
	suppress_callback_exceptions=True
)

server = app.server

register_app_callbacks(app)

app.layout = html.Div(className="master-container", children=[
	sidebar(),
	html.Div(className="page-container", children=[
		titlebar(),
		dash.page_container])
	])

if __name__ == "__main__":
	app.run(debug=True, port="8050")
