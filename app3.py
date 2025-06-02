from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash import html
from dash import Dash, dcc, html

app = Dash(__name__)

#Dropdown cria uma caixa interativa com opções para o usuário
app.layout = html.Div([
        dcc.Dropdown(options=[{'label': color, 'value': color} #Options para colocar as opções
                            for color in ['blue', 'green', 'yellow']]),
        html.Div()
                 
    ])

def display_selected_color(color):
            if color is None:
                color = 'nothing'
            return 'You selected ' + color

if __name__ == '__main__':
    app.run(port=8050)

    
