import dash
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme
import pandas as pd
import requests
from io import BytesIO

# external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]
# external_stylesheets = [dbc.themes.GRID, 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Covid-19 v okresech'
server = app.server
app.config.suppress_callback_exceptions = True
decimal_format = Format(precision=2, scheme=Scheme.decimal)
offline_data_mode = False
PATHS_TO_DB_FILES = {'dff': 'data/dff.pkl'}

if offline_data_mode:
    # offline data acquisition
    dff = pd.read_pickle(PATHS_TO_DB_FILES['dff'])

else:
    # online data acquisition
    try:
        link = 'https://docs.google.com/spreadsheets/d/1FFEDhS6VMWon_AWkJrf8j3XxjZ4J6UI1B2lO3IW-EEc/export?format=csv&id=1FFEDhS6VMWon_AWkJrf8j3XxjZ4J6UI1B2lO3IW-EEc&gid=1011737151'
        r = requests.get(link)
        data = r.content
        # print('-- DATA QUERY EXECUTED --')

        # get data in wide format
        df = pd.read_csv(BytesIO(data))
        df = df.set_index(['Kraj', 'Okres']).T
        df = df.dropna()
        # df = df.drop(index='Kontrola')
        # df = df.drop(index='Změna')
        df.index.rename(name='Datum', inplace=True)

        # wide to long
        dff = df.stack(level=['Kraj', 'Okres'])
        dff = pd.DataFrame(dff)
        dff.reset_index(inplace=True)
        dff.rename(columns={0: 'Nakažení'}, inplace=True)

        # explicitly setting types
        dff['Datum'] = dff['Datum'].astype('datetime64')
        dff['Nakažení'] = dff['Nakažení'].astype('int64')

    except:
        # offline data acquisition
        dff = pd.read_pickle(PATHS_TO_DB_FILES['dff'])

# prepare df for table
df1 = dff[dff.Datum == dff.Datum.max()]
df2 = dff[dff.Datum == (dff.Datum.max() - pd.Timedelta(days=3))]
df1.set_index(keys=['Okres'], inplace=True)
df2.set_index(keys=['Okres'], inplace=True)
df_table = df1.copy()
df_table['Přírůstek'] = (df1['Nakažení'] - df2['Nakažení']) / df2['Nakažení'] * 100
df_table.drop(columns=['Datum', 'Kraj'], inplace=True)
df_table.sort_values(by='Přírůstek', ascending=False, inplace=True)
df_table.reset_index(inplace=True)

districts = df_table['Okres'].unique()
