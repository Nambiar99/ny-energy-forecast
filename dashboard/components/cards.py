from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

def time_card(card_id, title, value, className):
	card = dbc.Card(dbc.CardBody([
		html.H6(str(title), className="card-title"),
		html.H2(id=card_id, children=value, className="card-value"),
	]), className=className)
	return card