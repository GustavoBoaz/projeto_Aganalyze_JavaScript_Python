from run import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

dfg = pd.read_csv('analyze/data_csv/_all2.csv')

REGIONALS = list(dfg.REGIONAL.unique())
CLIENTES = list(dfg.CLIENTE.unique())
ANOS = list(dfg.ANO.unique())

fig3 = px.scatter(dfg, x="SLA DENTRO DO PRAZO", y="SLA FORA DO PRAZO", color="CLIENTE", height=780, template="plotly_dark")

app.layout = html.Div([
    html.Div([
        html.Br([]),
        html.H3('FECHAMENTO MENSAL (TODOS OS CLIENTES)'),      
    ], className="banner"),

    html.Div([
        html.Div([
                html.Br([]),
                dcc.Graph(id="graph1")
            ], className=""),

        dcc.Slider(
            id='mes-slider', min=1, max=12, step=1, value=1,
            marks={1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'},
        ),

        dcc.Slider(
            id='ano-slider', min=2015, max=2019, step=1, value=2015,
            marks={2015:'2015', 2016:'2016', 2017:'2017', 2018:'2018', 2019:'2019'},
        ),
    ], className="row"),

    html.Div([

        html.Div([
            html.Br([]),
            html.H3('FECHAMENTO MENSAL REGIONAL / CLIENTE'),
        ], className=""),

        html.Br([]),
        dcc.Dropdown(
            id='regional-dropdown',
            options=[{'label':reional, 'value':reional} for reional in REGIONALS],
            placeholder="Regional"),
        
        html.Br([]),
        dcc.Dropdown(
            id='cliente-dropdown',
            options=[{'label':cliente, 'value':cliente} for cliente in CLIENTES],
            placeholder="Cliente"),
        
        html.Br([]),
        dcc.Dropdown(
            id='ano-dropdown',
            options=[{'label':ano, 'value':ano} for ano in ANOS],
            placeholder="Ano desejado",
            value=''),

        html.Br([]),
        html.Div([
                dcc.Graph(id="graph2")
            ], className=""),
        html.Br([]),
        html.Br([]),
        html.Br([]),
    ], className="five columns"),

    html.Div([

        html.Div([
            html.Br([]),
            html.H3('SLA CLIENTES EM GERAL'),
        ], className=""),

        html.Br([]),
        html.Div([
                dcc.Graph(figure=fig3)
            ], className=""),
        html.Br([]),
        html.Br([]),
        html.Br([]),
    ], className="six columns"),
])

app.css.append_css({
    "external_url":"https://codepen.io/chriddy/pen/bWLwgP.css"
})

@app.callback(
    Output("graph1", "figure"),
    [
        Input("mes-slider", "value"),
        Input("ano-slider", "value")
    ])
def update_graph1(mes, ano):
    
    df = pd.read_csv('analyze/data_csv/_all.csv')
    fig = px.scatter(
        df.query("ANO=="+str(ano)+" & MES=="+str(mes)+""), 
        x="SLA DENTRO DO PRAZO",
        y="SLA FORA DO PRAZO",
        size="QUANTIDADE DE CHAMADOS",
        color="REGIONAL",
        log_x=True,
        size_max=100,
        height=710,
        template="plotly_dark")
    return fig

@app.callback(
    Output("graph2", "figure"),
    [
        Input("regional-dropdown", "value"),
        Input("cliente-dropdown", "value"),
        Input("ano-dropdown", "value")
    ])
def update_graph2(regional, cliente, ano):

    df = pd.read_csv('analyze/data_csv/_all2.csv')

    dic = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}
    df.MES = [dic[mes] for mes in df.MES]

    fig2 = px.bar_polar(
        df[(df.REGIONAL == regional) & (df.CLIENTE == cliente) & (df.ANO == ano)], 
        r="QUANTIDADE DE CHAMADOS",
        theta="MES",
        color="MES",
        template="plotly_dark",
        color_discrete_sequence= px.colors.sequential.Plotly3[-3::-1])
    return fig2