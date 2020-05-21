import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# --- DEFINE LAYOUT
layout = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
            ###### Soubory Cookies a ochrana vašeho soukromí
            
            Tento web využívá službu Google Analytics, což je analytická služba poskytovaná společností Google Inc. („Google“). Google Analytics používá tzv. „cookies“, textové soubory, které se ukládají ve vašem počítači a umožňují analýzu vašeho používání webové stránky za účelem zlepšování služeb tohoto webu. Přitom však nedochází k vaší identifikaci. I vaše IP adresa je zpracována pouze ve zkrácené podobě, což znemožňuje vaši identifikaci.

            Všechny standardní prohlížeče Vám umožňují nastavit, zda se budou cookies na vašem počítači ukládat, a umožňují Vám vymazat již uložené cookies. Kromě toho můžete použití Google Analytics zakázat použitím doplňku dostupného z [tools.google.com/dlpage/gaoptout](https://tools.google.com/dlpage/gaoptout).
            
            Pokud máte ukládání cookies povolené a navštívíte naše webové stránky, souhlasíte tím s používáním cookies podle těchto informací a podle podmínek Google Analytics.
            
            Bližší informace o podmínkách používání a ochraně dat v souvislosti se službou Google Analytics naleznete na adrese [www.google.com/analytics](https://marketingplatform.google.com/about/analytics/). Tento web používá rozšíření „anonymizeIp“, takže jsou IP adresy zpracovávány pouze zkráceně, aby se vyloučila přímá osobní identifikovatelnost.
            ''')
        ])
    ])
])
