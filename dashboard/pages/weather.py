import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.cards import time_card

dash.register_page(__name__, path="/weather", name="weather", order=2)

layout = html.Div(className="page-container", children=[
	dcc.Interval(id="temp-interval", interval=60*60*1000, n_intervals=0),
	html.Div(className="weather-first-row-container", children=[
			dcc.Graph(id="temp-graph", className="weather-graph-container"),
			dcc.Graph(id="humidity-graph", className="weather-graph-container"),
		]),
	html.Div(className="weather-first-row-container", children=[
				dcc.Graph(id="wind-graph", className="weather-graph-container"),
				dcc.Graph(id="pressure-graph", className="weather-graph-container"),
		])
])


