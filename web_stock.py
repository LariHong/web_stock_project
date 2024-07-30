import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
from datetime import timedelta
import numpy as np

app = dash.Dash(__name__)

# 读取数据并提取日期范围
data = pd.read_csv('1234.csv')
data['Date'] = pd.to_datetime(data['Date'])
min_date = data['Date'].min()
max_date = data['Date'].max()

def generate_date_options(start_date, end_date):
    years = range(start_date.year, end_date.year + 1)
    months = range(1, 13)
    days = range(1, 32)  # 默认最多31天

    year_options = [{'label': str(year), 'value': year} for year in years]
    month_options = [{'label': f'{month:02}', 'value': month} for month in months]
    day_options = [{'label': f'{day:02}', 'value': day} for day in days]

    return year_options, month_options, day_options

year_options, month_options, day_options = generate_date_options(min_date, max_date)

app.layout = html.Div(
    style={'width': '80%', 'margin': 'auto', 'border': '2px solid black'},
    children=[
        html.Div(
            children=html.H1("预测台股"),
            style={'textAlign': 'center', 'padding': '10px'}
        ),
        html.Div(
            style={'border': '2px solid green', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Label('股票代码:', style={'margin-right': '10px'}),
                dcc.Input(id='stock-code', type='text', value='1234', style={'margin-right': '20px'})
            ]
        ),
        html.Div(
            style={'border': '2px solid blue', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '10px'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'align-items': 'center', 'width': '100%'},
                            children=[
                                html.Label('开始年:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='start-year-dropdown',
                                    options=year_options,
                                    value=min_date.year,
                                    clearable=False,  # 禁用清除功能
                                    style={'width': '100px', 'margin-right': '10px'}  # 设置宽度和间距
                                ),
                                html.Label('开始月:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='start-month-dropdown',
                                    options=month_options,
                                    value=min_date.month,
                                    clearable=False,  # 禁用清除功能
                                    style={'width': '100px', 'margin-right': '10px'}  # 设置宽度和间距
                                ),
                                html.Label('开始日:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='start-day-dropdown',
                                    options=day_options,
                                    value=min_date.day,
                                    clearable=False,  # 禁用清除功能
                                    style={'width': '100px'}  # 设置宽度
                                ),
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-between'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'align-items': 'center', 'width': '100%'},
                            children=[
                                html.Label('结束年:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='end-year-dropdown',
                                    options=year_options,
                                    value=max_date.year,
                                    clearable=False,  # 禁用清除功能
                                    style={'width': '100px', 'margin-right': '10px'}  # 设置宽度和间距
                                ),
                                html.Label('结束月:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='end-month-dropdown',
                                    options=month_options,
                                    value=max_date.month,
                                    clearable=False,  # 禁用清除功能
                                    style={'width': '100px', 'margin-right': '10px'}  # 设置宽度和间距
                                ),
                                html.Label('结束日:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='end-day-dropdown',
                                    options=day_options,
                                    value=max_date.day,
                                    clearable=False,  # 禁用清除功能
                                    style={'width': '100px'}  # 设置宽度
                                ),
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            style={'display': 'flex', 'justify-content': 'space-around', 'border': '2px solid yellow', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Div(
                    children=[dcc.Graph(id='k-line-chart', style={'height': '400px', 'width': '100%'})],
                    style={'width': '45%', 'border': '2px solid orange', 'padding': '10px'}
                ),
                html.Div(
                    children=[dcc.Graph(id='macd-chart', style={'height': '400px', 'width': '100%'})],
                    style={'width': '45%', 'border': '2px solid orange', 'padding': '10px'}
                )
            ]
        ),
        html.Div(
            style={'border': '2px solid brown', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-around', 'padding': '10px'},
                    children=[
                        html.Div(
                            html.Label('热力图:', style={'margin-right': '10px'}),
                        )
                    ]
                ),
                html.Div(
                    children=[dcc.Graph(id='heatmap-chart')],
                    style={'border': '2px solid brown', 'padding': '10px'}
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
                                    id='analysis-radio',
                                    options=[
                                        {'label': '分类', 'value': 'classification'},
                                        {'label': '回归', 'value': 'regression'}
                                    ],
                                    value='classification',
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

@app.callback(
    Output('k-line-chart', 'figure'),
    Output('macd-chart', 'figure'),
    Output('heatmap-chart', 'figure'),
    Input('stock-code', 'value'),
    Input('start-year-dropdown', 'value'),
    Input('start-month-dropdown', 'value'),
    Input('start-day-dropdown', 'value'),
    Input('end-year-dropdown', 'value'),
    Input('end-month-dropdown', 'value'),
    Input('end-day-dropdown', 'value'),
)
def update_charts(stock_code, start_year, start_month, start_day, end_year, end_month, end_day):
    start_date = pd.Timestamp(year=start_year, month=start_month, day=start_day)
    end_date = pd.Timestamp(year=end_year, month=end_month, day=end_day)
    
    data = pd.read_csv(f"{stock_code}.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    
    fig_candlestick = create_candlestick_chart(data)
    fig_macd = create_macd_chart(data)
    fig_heatmap = create_heatmap_chart(data)
    
    return fig_candlestick, fig_macd, fig_heatmap

def create_candlestick_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick'
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['upperband'],
        mode='lines',
        name='Upper Band',
        line=dict(color='blue', width=1, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['ma'],
        mode='lines',
        name='Price (MA)',
        line=dict(color='black', width=1)
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['lowerband'],
        mode='lines',
        name='Lower Band',
        line=dict(color='red', width=1, dash='dash')
    ))
    fig.update_layout(
        title='K线图与折线图',
        xaxis_title='日期',
        yaxis_title='价格',
        xaxis_rangeslider_visible=False,
        autosize=True
    )
    return fig

def create_macd_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['MACD'],
        mode='lines',
        name='MACD',
        line=dict(color='red')
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Signal_Line'],
        mode='lines',
        name='Signal Line',
        line=dict(color='yellow')
    ))
    fig.add_trace(go.Bar(
        x=data['Date'],
        y=data['MACD_Histogram'],
        name='MACD Histogram',
        marker=dict(color=['red' if val >= 0 else 'green' for val in data['MACD_Histogram']]),
        opacity=0.7
    ))
    fig.update_layout(
        title='MACD Chart',
        xaxis_title='日期',
        yaxis_title='MACD',
        autosize=True
    )
    return fig

def create_heatmap_chart(data):
    # 示例数据和生成方式，替换为实际的数据处理
    corr_matrix = data.iloc[:, 1:].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title='热力图',
        xaxis_title='特征',
        yaxis_title='特征',
        autosize=True,
        xaxis=dict(
            showgrid=True,  # 显示网格线
            gridcolor='black',  # 网格线颜色
            gridwidth=0.5  # 网格线宽度
        ),
        yaxis=dict(
            showgrid=True,  # 显示网格线
            gridcolor='black',  # 网格线颜色
            gridwidth=0.5  # 网格线宽度
        )
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
