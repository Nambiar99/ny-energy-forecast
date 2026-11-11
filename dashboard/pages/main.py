import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.cards import time_card
from components.bars import menubar

dash.register_page(__name__, path="/", name="main", order=1)

layout = html.Div(className="main-page-container", children=[
	html.H2("Dashboard", className="page-title"),
	dcc.Interval(id="time-interval", interval=1*1000, n_intervals=0),
	dcc.Interval(id="graph-interval", interval=60*60*1000, n_intervals=0),
	html.Div(className="time-bar-container", children=[
		time_card(card_id="nyc-time", title="Time", value="1", className="card-container"),
	]),
	html.Div(className="first-row-container", children=[
		dcc.Graph(id="forecast-graph", className="graph-container"),
	])
	
])


