import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd

from dash_app.app import app, districts, df_table, decimal_format

# --- DEFINE LAYOUT
row_graph = dbc.Row([
	dbc.Col([
		# dcc.Loading(
		# 	id='loading_plot_districts',
		# 	children=[
		dcc.Graph(
			id='plot_districts',
			figure={},
			style={'height': 600}
		)
		# 	]
		# )
	])
])

row_temp_div = dbc.Row([
	dbc.Col([
		html.Div(
			id='temp_div',
			children=[],
			style={'whiteSpace': 'pre-wrap'}
		)
	])
])

row_table = dbc.Row([
	dbc.Col([
		dash_table.DataTable(
			id='table_districts',
			columns=[
				{'name': 'Okres', 					'id': 'Okres', 		'type': 'text'},
				{'name': 'Nakažení', 				'id': 'Nakažení', 	'type': 'numeric'},
				{'name': 'Přírůstek (3 dny) [%]', 	'id': 'Přírůstek', 	'type': 'numeric', 'format': decimal_format},
			],
			data=df_table.to_dict('records'),
			row_selectable='multi',
			row_deletable=False,
			selected_rows=[0, 1, 2, 3, 4],
			sort_action='native',
			sort_mode='multi',
			style_table={
				'height': '100%',
				# 'overflowY': 'scroll'
			},
			fixed_rows={'headers': True, 'data': 0},
			# style_cell={'width': '100px'},
			style_cell_conditional=[
				{'if': {'column_id': 'Okres'}, 		'textAlign': 'left'},
				{'if': {'column_id': 'Okres'}, 		'width': '40%'},
				{'if': {'column_id': 'Nakažení'}, 	'width': '20%'},
				{'if': {'column_id': 'Přírůstek'}, 	'width': '30%'}
			]
		)
	])
])

row_credits = dbc.Row([
	dbc.Col([
		# author
		html.Div([
			html.A('vaclav.sisl@gmail.com', href='mailto:vaclav.sisl@gmail.com', target='_blank')
		])
	], width=2),

	dbc.Col([
		# data
		html.Div([
			html.A('Data', href='https://docs.google.com/spreadsheets/d/1FFEDhS6VMWon_AWkJrf8j3XxjZ4J6UI1B2lO3IW-EEc/edit?usp=sharing', target='_blank')
		])
	], width=1),

	dbc.Col([
		# github
		html.Div([
			html.A('Github', href='https://github.com/vsisl/Covid19_cz_districts', target='_blank')
		])
	], width=1)
], justify='end')

layout = html.Div([
	dbc.Row([
		dbc.Col([
			row_graph,
			row_temp_div
		], width=7),

		dbc.Col([
			row_table,
		], width=5)
	]),
	row_credits
])