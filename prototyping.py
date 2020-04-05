# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 13:18:33 2020

@author: vacla
"""

import pandas as pd
# import gspread
import requests
from io import BytesIO

link = 'https://docs.google.com/spreadsheets/d/1FFEDhS6VMWon_AWkJrf8j3XxjZ4J6UI1B2lO3IW-EEc/export?format=csv&id=1FFEDhS6VMWon_AWkJrf8j3XxjZ4J6UI1B2lO3IW-EEc&gid=1011737151'
r = requests.get(link)
data = r.content

# get data in wide format
df = pd.read_csv(BytesIO(data))
df = df.set_index(['Kraj', 'Okres']).T
df = df.dropna()
df = df.drop(index='Kontrola')
df.index.rename(name='Datum', inplace=True)

# store
df.to_pickle('data/df.pkl')

# wide to long
dff = df.stack(level=['Kraj', 'Okres'])
dff = pd.DataFrame(dff)
dff.reset_index(inplace=True)
dff.rename(columns={0: 'Nakažení'}, inplace=True)

# explicitly setting types
dff['Datum'] = dff['Datum'].astype('datetime64')
dff['Nakažení'] = dff['Nakažení'].astype('int64')

# test filtering
df['Jihočeský kraj', 'Strakonice']
dff[(dff['Kraj'] == 'Jihočeský kraj') & (dff['Okres'] == 'Strakonice')]

# store
dff.to_pickle('data/dff.pkl')

# -------------------------------

import plotly.express as px
from plotly.offline import plot

fig = px.line(dff[dff['Kraj'] == 'Jihočeský kraj'], x='Datum', y='Nakažení', line_group='Okres', color='Okres', hover_name='Okres')


plot(fig)


# -------------------------------

dff = pd.read_pickle('data/dff.pkl')
districts = dff['Okres'].unique().sort()


dff['Proc. Přírůstek'] = 



dff.Datum.max()


df1 = dff[dff.Datum == dff.Datum.max()]
df2 = dff[dff.Datum == (dff.Datum.max() - pd.Timedelta(days=1))]

df1.set_index(keys=['Okres'], inplace=True)
df2.set_index(keys=['Okres'], inplace=True)

df_table = df1.copy()
df_table['Přírůstek [%]'] = (df1['Nakažení'] - df2['Nakažení']) / df2['Nakažení'] * 100
df_table.drop(columns=['Datum', 'Kraj'], inplace=True)
df_table.reset_index(inplace=True)





















