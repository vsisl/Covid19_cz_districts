import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import socket
import os
import sys

sys.path.append(os.getcwd())

# for pth in sys.path:
# 	print(pth)

from dash_app.app import app
from dash_app.pages import prototyping_layout
from dash_app.pages import prototyping_callbacks     # this import statement has to be here even though callbacks are not explicitly used

# styles = {'link': {'padding': '20'}}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    dbc.Row([
        dbc.Col(html.H3('Covid-19 v okresech')),
    ], justify='start'),

    html.Div(id='page_content')
], style={'width': '98%'})


@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dev':
        return prototyping_layout.layout
    else:
        return prototyping_layout.layout


if __name__ == '__main__':
    # hostname = socket.gethostname()
    # ip_address = socket.gethostbyname(hostname)
    # app.run_server(host=ip_address, port=5002, debug=True)
    app.run_server(host='0.0.0.0', port=5002, debug=True)