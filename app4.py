import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Criação do app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Leitura do JSON
with open(r'C:\Users\mathe\Desktop\Estágio\dash_intro\12h03m42s.json', 'r') as f:
    json_data = json.load(f)

# Processamento dos dados
event_files = json_data["eventFiles"]
cf_list = []

for event_id, event_data in event_files.items():
    cf_items = event_data.get("df", {}).get("cf", [])
    for item in cf_items:
        cf_list.append({
            "eventId": event_id,
            "chName": item["chName"],
            "peak": item["peak"],
            "rms": item["rms"],
            "value": item["value"]
        })

df_cf = pd.DataFrame(cf_list)

# Layout do app
app.layout = dbc.Container([
    html.H1('Análise de Eventos', className='text-center mb-4'),
    
    html.H5('Gráficos de linha dos picos de frequência por canal (T, R, V)', 
            className='text-center mb-4'),

    dbc.Tabs([
        dbc.Tab(label="Componente T", tab_id='T'),
        dbc.Tab(label="Componente R", tab_id='R'),
        dbc.Tab(label="Componente V", tab_id='V'),
    ], id='tabs', active_tab='T', className='mb-4'),

    dcc.Graph(id='grafico_metricas'),

    html.Hr(),

    html.Div(id='estatisticas', className='text-center mt-4')
], fluid=True)

# Callback para atualizar os gráficos
@app.callback(
    Output('grafico_metricas', 'figure'),
    Input('tabs', 'active_tab')
)
def update_graph(active_tab):
    df_filtrado = df_cf[df_cf['chName'] == active_tab]

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Pico", "RMS", "Fator")
    )

    fig.add_trace(go.Scatter(
        x=df_filtrado['eventId'], y=df_filtrado['peak'],
        mode='lines+markers', name='Pico'), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df_filtrado['eventId'], y=df_filtrado['rms'],
        mode='lines+markers', name='RMS'), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=df_filtrado['eventId'], y=df_filtrado['value'],
        mode='lines+markers', name='Fator'), row=3, col=1)

    fig.update_layout(
        height=800,
        title_text=f"Métricas - Componente {active_tab}",
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)
