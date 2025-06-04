from dash import Dash, html, Input, Output, dcc, dash_table
import dash_bootstrap_components as dbc
import json
import pandas as pd

# Definindo app, e tema FLATLY
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Lendo o arquivo em JSON 
with open(r'C:\Users\mathe\Desktop\Estágio\dash_intro\12h03m42s.json', 'r') as f:
    json_data = json.load(f)

event_files = json_data["eventFiles"] # Acessando no JSON, os eventFiles.
cf_list = [] # Criando uma lista vazia

for event_id, event_data in event_files.items(): # Para cada event_id e event_data em event_files, pegando os itens, faça:
    cf_items = event_data.get("df", {}).get("cf", []) # cf_items acessa a lista de métricas agregadas (cf) de cada estação. Usa .get() com {} e [] como segurança para evitar erro caso alguma chave falte.
    for item in cf_items:
        cf_list.append({ # Adicionando um dicionário com os dados de cada canal (T, R ou V) de cada evento.
            "eventId": event_id, # O conteudo de event_id
            "Componente": item["chName"], # de nome do canal.
            "Pico": item["peak"], # Pico
            "RMS": item["rms"], # O RMS
            "Fator": item["value"] # value
        })

# Transformando o cf_list em um data Frame.
df_cf = pd.DataFrame(cf_list)

app.layout = dbc.Container([  # Criando o layout
    html.H1("Tabela dos picos de frequência por canal (T, R, V)", className="text-center mb-4", style={'marginBottom': '30px'}), # Criando h1

    # Criando abas de componentes, cada db.Tab é uma aba clicavél
    dbc.Tabs([
        dbc.Tab(label="Componente T", tab_id="T"), # aba do componente T, com id T
        dbc.Tab(label="Componente R", tab_id="R"), # Aba do componente R, com id R
        dbc.Tab(label="Componente V", tab_id="V"), # Aba do componente V, com id V
    ], id="tabs", active_tab="T", className="mb-4"), # Por default, a aba inicial será a T

    dash_table.DataTable( # Criando a tabela, 
        id="tabela_metricas", # Definindo id tabela_metricas
        columns=[ # Definindo as colunas da tabela
            {"name": "eventId", "id": "eventId"}, 
            {"name": "Componente", "id": "Componente"},
            {"name": "Pico", "id": "Pico", "type": "numeric", "format": {"specifier": ".6f"}},
            {"name": "RMS", "id": "RMS", "type": "numeric", "format": {"specifier": ".6f"}},
            {"name": "Fator", "id": "Fator", "type": "numeric", "format": {"specifier": ".6f"}},
        ],
        style_data_conditional=[
            {
            'if': {'filter_query': '{Pico} > 0.3'},
            'backgroundColor': '#FFCDD2',
            'color': 'black'
            }
        ],

        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'}, # Definindo o estilo da celula alinhanda ao centro
        filter_action="native", # Filtro é o nativo da tabela
        sort_action="native", # Ação de seleção também é o nativo
        page_size=10, # Tamanho da pg
        style_header={'backgroundColor': '#DCE3EA', 'fontWeight': 'bold'}, # Definindo, cores de bachground, e estilo de fonte
        export_format="csv", # Botão para exportar em csv
    )
], fluid=True)

# Definindo o Callback, responsividade do app.
@app.callback(
    Output("tabela_metricas", "data"), # Saída
    Input("tabs", "active_tab") # Entrada para o callback
)
def atualizar_tabela(componente): # Função para atualizar a tabela na troca de aba.
    return df_cf[df_cf["Componente"] == componente].to_dict("records")


# Rodar o app.
if __name__ == "__main__":
    app.run(debug=True)
