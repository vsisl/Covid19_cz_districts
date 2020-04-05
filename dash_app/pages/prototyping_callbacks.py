from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
from dash_table.Format import Format, Scheme, Sign, Symbol
import pandas as pd
import plotly.express as px

from dash_app.app import app, districts, dff


# @app.callback(
#     Output('temp_div', "children"),
#     [Input('table_districts', "derived_virtual_selected_rows"),
#      Input('table_districts', "derived_virtual_selected_row_ids"),
#      Input('table_districts', "selected_rows"),
#      Input('table_districts', "selected_row_ids")])
# def update_temp_div(derived_virtual_selected_rows, derived_virtual_selected_row_ids, selected_rows, selected_row_ids):
#     # When the table is first rendered, `derived_virtual_data` and
#     # `derived_virtual_selected_rows` will be `None`. This is due to an
#     # idiosyncracy in Dash (unsupplied properties are always None and Dash
#     # calls the dependent callbacks when the component is first rendered).
#     # So, if `rows` is `None`, then the component was just rendered
#     # and its value will be the same as the component's dataframe.
#     # Instead of setting `None` in here, you could also set
#     # `derived_virtual_data=df.to_rows('dict')` when you initialize
#     # the component.
#     if derived_virtual_selected_rows is None:
#         derived_virtual_selected_rows = ['asdaaaaaaaaaaaaaaaaa']
#
#     text_to_return = f"""
#         derived_virtual_selected_rows = {str(derived_virtual_selected_rows)}
#         derived_virtual_selected_row_ids = {str(derived_virtual_selected_row_ids)}
#         selected_rows = {str(selected_rows)}
#         selected_row_ids = {str(selected_row_ids)}
#         Okresy = {str(districts[selected_rows])}
#         {str(type(districts[selected_rows]))}
#     """
#     return text_to_return


@app.callback(
    Output('plot_districts', 'figure'),
    [Input('table_districts', "selected_rows")])
def update_plot(selected_rows):
    # if selected rows is empty list
    if len(selected_rows) == 0:
        fig = {}

    else:
        fig = px.line(dff[dff['Okres'].isin(districts[selected_rows])], x='Datum', y='Nakažení', line_group='Okres', color='Okres', hover_name='Okres')

    return fig
