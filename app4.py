from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import json

# ========== LEITURA DO JSON ==========
with open(r'C:\Users\mathe\Desktop\Estágio\dash_intro\12h03m42s.json', 'r') as f:
    json_data = json.load(f)

sensor_data = json_data['eventFiles']["20160008"]
peak_data = sensor_data["dfFft"]["peak"]


colors = {
    'background': '#111111',
    'text': '#111111'
}

# ========== TRANSFORMAÇÃO EM DATAFRAME ==========
dados = []

for canal in peak_data:
    nome_canal = canal["chName"]
    for ponto in canal["value"]:
        dados.append({
            "Canal": nome_canal,
            "Frequência": ponto["freq"],
            "Amplitude": ponto["ampl"]
        })

df_peak = pd.DataFrame(dados)

# ========== SEPARA OS GRÁFICOS POR CANAL ==========
graficos = []

for canal in df_peak["Canal"].unique():
    df_canal = df_peak[df_peak["Canal"] == canal]
    fig = px.line(
        df_canal,
        x="Frequência",
        y="Amplitude",
        markers=True,
        title=f"Picos de Frequência - Canal {canal}"
    )
    fig.update_layout(
        xaxis_title="Frequência (Hz)",
        yaxis_title="Amplitude",
        legend_title="Canal"
    )
    graficos.append(dcc.Graph(figure=fig))

# ========== DASH APP ==========
app = Dash()

app.layout = html.Div(
    children=[
        html.H1(children='Análise de Picos de Frequência', style={'textAlign': 'center', 'color': colors['text']}),
        html.Div(
            children='Gráficos de linha dos picos de frequência por canal (T, R, V)',
            style={'textAlign': 'center', 'color': colors['text']}  # Corrigido aqui
        ),
        *graficos
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
