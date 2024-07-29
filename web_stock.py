import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

app.layout = html.Div(
    style={'width': '80%', 'margin': 'auto', 'border': '2px solid black'},
    children=[
        # Title
        html.Div(
            children=html.H1("預測台股"),
            style={'textAlign': 'center', 'padding': '10px'}
        ),
        # Input Section
        html.Div(
            style={'border': '2px solid green', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Label('股票代號:', style={'margin-right': '10px'}),
                dcc.Input(id='stock-code', type='text', value='2330', style={'margin-right': '20px'}),
                html.Label('起始時間:', style={'margin-right': '10px'}),
                dcc.Input(id='start-date', type='text', value='2024/03/01', style={'margin-right': '20px'}),
                html.Label('結束時間:', style={'margin-right': '10px'}),
                dcc.Input(id='end-date', type='text', value='2024/05/31')
            ]
        ),
        # Chart Section
        html.Div(
            style={'display': 'flex', 'justify-content': 'space-around', 'border': '2px solid yellow', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Div(
                    children=[dcc.Graph(id='k-line-chart')],
                    style={'width': '45%', 'border': '2px solid orange', 'padding': '10px'}
                ),
                html.Div(
                    children=[dcc.Graph(id='macd-chart')],
                    style={'width': '45%', 'border': '2px solid orange', 'padding': '10px'}
                )
            ]
        ),
        # Analysis Section
        html.Div(
            style={'border': '2px solid brown', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-around', 'padding': '10px'},
                    children=[
                        html.Div(
                            children=[
                                dcc.RadioItems(
                                    id='heatmap-radio',
                                    options=[
                                        {'label': '熱力圖', 'value': 'heatmap'},
                                        {'label': '分類', 'value': 'classification'},
                                        {'label': '回歸', 'value': 'regression'}
                                    ],
                                    value='heatmap',
                                    labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                                ),
                                dcc.Dropdown(
                                    id='feature-dropdown',
                                    options=[{'label': f'Feature {i}', 'value': f'feature_{i}'} for i in range(1, 11)],
                                    value='feature_1'
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    children=[dcc.Graph(id='analysis-chart')],
                    style={'border': '2px solid brown', 'padding': '10px'}
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
