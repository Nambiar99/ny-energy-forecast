from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

def sidebar():
	bar = html.Div(className="sidebar-container", children=[
		html.Div(className="sidebar-content", children=[
			# html.P("NY Energy Predictor", className="sidebar-title"),
			dbc.Nav([
				dbc.NavLink("Dashboard", href="/", className="sidebar-pill", active="exact"),
				dbc.NavLink("Weather", href="/weather", className="sidebar-pill", active="exact")
			], vertical=True, className="sidebar-pill-container")
		])
	])
	return bar

def titlebar():
	bar = html.Div(className="titlebar-container", children=[
		html.P(className="titlebar-title", children="New York Energy Predictor")
	])
	return bar

def menubar():
	options=[
		{"label": "LightGBM", "value": "LightGBM"},
		{"label": "LSTM", "value": "LSTM"}
	]
	bar = dcc.Checklist(
		id="model-checkbox",
		options=options,
		inline=False,
		className="menubar-container",
		labelClassName="menubar-options"
	)
	return bar

