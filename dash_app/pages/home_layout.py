import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

from dash_app.app import df_table, decimal_format, dcc_transparent_loading

# --- DEFINE LAYOUT
row_graph = dbc.Row([
	dbc.Col([
		dcc_transparent_loading(
			loading_id='loading_plot_districts',
			loading_children=[
				dcc.Graph(
					className='dash-graph-districts',
					id='plot_districts',
					figure={},
					config={
						'displaylogo': False,
						'modeBarButtonsToRemove': ['toImage', 'zoomIn2d', 'zoomOut2d', 'resetScale2d'],
					},
					# style={'height': 600}
				)
			]
		)
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
			fixed_rows={'headers': True, 'data': 0},
			style_table={'height': 600, 'maxHeight': 600},
			style_cell_conditional=[
				{'if': {'column_id': 'Okres'}, 		'textAlign': 'left'},
				{'if': {'column_id': 'Okres'}, 		'width': '30%'},
				{'if': {'column_id': 'Nakažení'}, 	'width': '20%'},
				{'if': {'column_id': 'Přírůstek'}, 	'width': '40%'}
			],
			style_data_conditional=[
				{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
			],
			style_header={
				'backgroundColor': 'rgb(230, 230, 230)',
				'fontWeight': 'bold',
				'height': 'auto',			# wrap text in case of overflow
				'whiteSpace': 'normal'
			},
			# export_columns='all',
			# export_format='xlsx',
			# export_headers='display'
		)
	])
])

row_credits = dbc.Row([
	dbc.Col([
		# author
		html.Div([
			html.A('Autor', href='https://www.linkedin.com/in/vaclav-sisl/', target='_blank')
		])
	], lg=1, width=12),

	dbc.Col([
		# data
		html.Div([
			html.A('Data', href='https://docs.google.com/spreadsheets/d/1FFEDhS6VMWon_AWkJrf8j3XxjZ4J6UI1B2lO3IW-EEc/edit?usp=sharing', target='_blank')
		])
	], lg=1, width=12),

	dbc.Col([
		# github
		html.Div([
			html.A('Github', href='https://github.com/vsisl/Covid19_cz_districts', target='_blank')
		])
	], lg=1, width=12),

	dbc.Col([
		# cookies
		html.Div([
			html.A('Soukromí a cookies', href='/cookies', target='_blank')
		])
	], lg=2, width=12)
], justify='end')

layout = html.Div([
	dbc.Row([
		dbc.Col([
			row_graph,
			row_temp_div
		], lg=7, width=12),

		dbc.Col([
			row_table,
		], lg=5, width=12)
	]),
	row_credits
])
