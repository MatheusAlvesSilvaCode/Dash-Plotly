import os
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# Pode ser add vários temas, como o SUPERHERO, BOOTSTRAP, MINTY, DARKLY

@app.callback(
    Output('output-text', 'children'),
    Input('input-dropdown', 'value')
)
def update_text(selected_value):
    return f"Você escolheu: {selected_value}"


if __name__ == '__main__':
    app.run(debug=True)