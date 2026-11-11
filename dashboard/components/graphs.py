import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from utils.forecast import forecast
from utils.forecast import fetch_weather_data

def energy_graph():
	plot_df, next_24h, lag, horizon = forecast()
	fig = go.Figure()
	fig.add_trace(go.Scatter(
		x=plot_df["Time"],
		y=plot_df["Demand"],
		mode="lines+markers",
		line=dict(color='#FF5A1F', width=3),
		name="From EIA"
	))
	fig.add_trace(go.Scatter(
		x=next_24h["Time"],
		y=next_24h["Demand"],
		mode="lines+markers",
		line=dict(color="#1F44FF", width=3),
		name="Predicted Demand"
	))
	fig.update_layout(
		margin=dict(l=70, r=30, t=70, b=0),
		title="Energy Demand Forecast",
		xaxis_title="Time",
		yaxis_title="Energy Demand (MW)",
		paper_bgcolor="rgba(0, 0, 0, 0)",
		plot_bgcolor="rgba(0, 0, 0, 0)",
		font_color="white",
		font=dict(family="arial"),
		legend=dict(
			orientation="h",
			x=0.5, y=1.1,
			xanchor="center", yanchor="bottom"
		)
	)
	fig.update_xaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)",
		type="date",
		dtick=60*60*1000,
		tickangle=0,
		tickformat="%H\n%b %d"
	)
	fig.update_yaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)"
	)
	return fig

def temp_graph():
	weather = fetch_weather_data(24)
	fig = go.Figure(go.Scatter(
		x=weather["Time"],
		y=weather["temperature_2m"],
		mode="lines+markers",
		line=dict(color="#FF5A1F", width=3),
		name="Temperature"
	))
	fig.update_layout(
		margin=dict(l=70, r=30, t=70, b=0),
		title="Temperature",
		xaxis_title="Time",
		yaxis_title="Temperature",
		paper_bgcolor="rgba(0, 0, 0, 0)",
		plot_bgcolor="rgba(0, 0, 0, 0)",
		font_color="white",
		font=dict(family="arial"),
		legend=dict(
			orientation="h",
			x=0.5, y=1.1,
			xanchor="center", yanchor="bottom"
		)
	)
	fig.update_xaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)",
		type="date",
		dtick=60*60*1000,
		tickangle=0,
		tickformat="%H\n%b %d"
		# tickformatstops=[
		# 	dict(dtickrange=[60*60*24*1000, None], value="%b %d"),
		# 	dict(dtickrange=[None, 60*60*24*1000], value="%H")
		# ]
	)
	fig.update_yaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)"
	)
	return fig

def humidity_graph():
	weather = fetch_weather_data(24)
	fig = go.Figure(go.Scatter(
		x=weather["Time"],
		y=weather["relative_humidity_2m"],
		mode="lines+markers",
		line=dict(color="#FF5A1F", width=3),
		name="Temperature"
	))
	fig.update_layout(
		margin=dict(l=70, r=30, t=70, b=0),
		title="Relative Humidity",
		xaxis_title="Time",
		yaxis_title="Relative Humidity",
		paper_bgcolor="rgba(0, 0, 0, 0)",
		plot_bgcolor="rgba(0, 0, 0, 0)",
		font_color="white",
		font=dict(family="arial"),
		legend=dict(
			orientation="h",
			x=0.5, y=1.1,
			xanchor="center", yanchor="bottom"
		)
	)
	fig.update_xaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)",
		type="date",
		dtick=60*60*1000,
		tickangle=0,
		tickformat="%H\n%b %d"
	)
	fig.update_yaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)"
	)
	return fig

def wind_graph():
	weather = fetch_weather_data(24)
	fig = go.Figure(go.Scatter(
		x=weather["Time"],
		y=weather["wind_speed_10m"],
		mode="lines+markers",
		line=dict(color="#FF5A1F", width=3),
		name="Temperature"
	))
	fig.update_layout(
		margin=dict(l=70, r=30, t=70, b=0),
		title="Wind Speed",
		xaxis_title="Time",
		yaxis_title="Wind Speed",
		paper_bgcolor="rgba(0, 0, 0, 0)",
		plot_bgcolor="rgba(0, 0, 0, 0)",
		font_color="white",
		font=dict(family="arial"),
		legend=dict(
			orientation="h",
			x=0.5, y=1.1,
			xanchor="center", yanchor="bottom"
		)
	)
	fig.update_xaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)",
		type="date",
		dtick=60*60*1000,
		tickangle=0,
		tickformat="%H\n%b %d"
	)
	fig.update_yaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)"
	)
	return fig

def pressure_graph():
	weather = fetch_weather_data(24)
	fig = go.Figure(go.Scatter(
		x=weather["Time"],
		y=weather["surface_pressure"],
		mode="lines+markers",
		line=dict(color="#FF5A1F", width=3),
		name="Temperature"
	))
	fig.update_layout(
		margin=dict(l=70, r=30, t=70, b=0),
		title="Surface Pressure",
		xaxis_title="Time",
		yaxis_title="Surface Pressure",
		paper_bgcolor="rgba(0, 0, 0, 0)",
		plot_bgcolor="rgba(0, 0, 0, 0)",
		font_color="white",
		font=dict(family="arial"),
		legend=dict(
			orientation="h",
			x=0.5, y=1.1,
			xanchor="center", yanchor="bottom"
		)
	)
	fig.update_xaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)",
		type="date",
		dtick=60*60*1000,
		tickangle=0,
		tickformat="%H\n%b %d"
	)
	fig.update_yaxes(
		showgrid=True,
		gridcolor="rgba(255, 255, 255, 0.2)"
	)
	return fig

