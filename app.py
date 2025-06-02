import os
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from jupyter_dash import JupyterDash

app = JupyterDash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# Pode ser add vários temas, como o SUPERHERO, BOOTSTRAP, MINTY, DARKLY

child1 = html.Div("Conteúdo da Coluna 1", style={'border': '1px solid white'})
child2 = dcc.Graph(figure=px.bar(x=[1, 2, 3], y=[4, 5, 6], title="Gráfico 1"))
child3 = html.Div("Conteúdo da Coluna 3", style={'color': 'red'})
child4 = dcc.Graph(figure=px.scatter(x=[10, 20, 30], y=[1, 2, 3], title="Gráfico 2"))

app.layout = html.Div(
    [
        # ... (seu código existente) ...
        dbc.Row(
            [
                dbc.Col(children=[child1, child2], lg=6, md=12),
                dbc.Col(children=[child3, child4], lg={'size': 6, 'offset': 4}, md=12)
            ]
        )
    ]
)         

if __name__ == '__main__':
    app.run(debug=True)

