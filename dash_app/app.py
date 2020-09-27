import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table.Format import Format, Scheme
import pandas as pd
import requests
from io import BytesIO

decimal_format = Format(precision=2, scheme=Scheme.decimal)
PATHS_TO_DB_FILES = {'dff': 'data/dff.pkl'}
offline_data_mode = False
apply_ga = True


def dcc_transparent_loading(loading_id, loading_children, loading_type='default'):
    """
    Returns dcc.Loading wrapped in html.Div(className='loading_wrapper').
    This html.Div has style defined in assets/custom.css giving dcc.Loading a transparent background.

    :param loading_id: str; is passed to dcc.Loading(id)
    :param loading_children: list; is passed to dcc.Loading(children)
    :param loading_type: str; {'graph', 'cube', 'circle', 'dot', 'default'}; is passed to dcc.Loading(type)
    :return: html.Div
    """
    transparent_loading = html.Div(
        className='loading_wrapper',
        children=[
            dcc.Loading(
                id=loading_id,
                type=loading_type,
                children=loading_children
            )
        ]
    )

    return transparent_loading


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)
app.title = 'Covid-19 v okresech'
server = app.server
app.config.suppress_callback_exceptions = True

if apply_ga:
    # adding Google Analytics with IP anonymization
    app.index_string = """<!DOCTYPE html>
    <html>
        <head>
            <!-- Global site tag (gtag.js) - Google Analytics -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=UA-167323389-1"></script>
            <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
    
                gtag('config', 'UA-167323389-1', { 'anonymize_ip': true });
            </script>
            <!-- Google Tag Manager -->
            <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
            new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            })(window,document,'script','dataLayer','GTM-P5FMPH3');</script>
            <!-- End Google Tag Manager -->
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
            <!-- Google Tag Manager (noscript) -->
            <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-P5FMPH3"
            height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
            <!-- End Google Tag Manager (noscript) -->
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>"""

# ------------------------
# --- DATA ACQUISITION ---
# ------------------------
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

        # originally, there would be no missing data (NaN) in the sheet
        # if a KHS would not publish new data (technically NaN), maintainers would copy over last valid value
        # but this changed recently => dropna() would cause dropping all days where at least one district has Nan value
        # df = df.dropna()
        # filling NaNs with last valid values
        df = df.fillna(method='ffill')

        # these two columns were originally present in the sheet but were removed later by maintainers
        # df = df.drop(index='Kontrola')
        # df = df.drop(index='Změna')

        df.index.rename(name='Datum', inplace=True)

        # wide to long
        dff = df.stack(level=['Kraj', 'Okres'], dropna=True)
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
