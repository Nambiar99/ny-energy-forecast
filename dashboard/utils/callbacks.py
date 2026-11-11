import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

import datetime
from datetime import UTC
from dash import Dash, dcc, html, Input, Output
from components.graphs import energy_graph, temp_graph, humidity_graph, wind_graph, pressure_graph


def register_app_callbacks(app):
	@app.callback(
		Output("nyc-time", "children"),
		Input("time-interval", "n_intervals")
	)
	def update_time(n):
		now = datetime.datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
		return now

	@app.callback(
		Output("forecast-graph", "figure"),
		Input("graph-interval", "n_intervals")
	)
	def make_graph(n):
		fig = energy_graph()
		return fig
	
	@app.callback(
		Output("temp-graph", "figure"),
		Output("humidity-graph", "figure"),
		Output("wind-graph", "figure"),
		Output("pressure-graph", "figure"),
		Input("temp-interval", "n_intervals")
	)
	def make_weather_graphs(n):
		temp_fig = temp_graph()
		humidity_fig = humidity_graph()
		wind_fig = wind_graph()
		pressure_fig = pressure_graph()
		return temp_fig, humidity_fig, wind_fig, pressure_fig