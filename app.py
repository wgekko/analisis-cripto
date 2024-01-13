
import ta
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from fetch_data import get_binance_data, data_extract
from fetch_graph import create_candles_plot

import warnings
warnings.simplefilter("ignore", category=FutureWarning)


app = dash.Dash(__name__, external_stylesheets= [dbc.themes.FLATLY] )

app.layout = html.Div([
    html.H1(['Evolución de valores de criptomonedas'], style={ 'textAlign': 'center','color': '#335EFF',  "font-weight": "bold",'margin-top': '35px','margin':'20px', 'margin-left':'50px'}),
    html.H2(['Gráficos para el análisis de técnicos'], style={ 'textAlign': 'center','color': '#335EFF', 'margin':'20px', 'margin-left':'40px'} ),
    html.Div([ 
        html.P(['Seleccione Cripto'], style={'margin-top': 45,'color': '#335EFF', 'margin-left':'30px'}),             
        dcc.Dropdown(
            id='coin-dropdown',
            options=[
                {'label': 'BTC', 'value': 'BTC'},
                {'label': 'ETH', 'value': 'ETH'},
                {'label': 'BNB', 'value': 'BNB'},
                {'label': 'ADA', 'value': 'ADA'},
                {'label': 'LTC', 'value': 'LTC'}
            ],
            value='BTC',
            style={'width': '40%', 'margin':'20px', 'margin-left':'20px'}
        ),
        html.P(['periodo de compresión'], style={'margin-top': 45,'color': '#335EFF'}),  
        dcc.Tabs(            
            id="tabs",
            value="1d",                   
            children=[                
                dcc.Tab(label="1 Hora", value="1h"),
                dcc.Tab(label="1 Dia", value="1d"),
                dcc.Tab(label="1 Semana", value="1w"),
                dcc.Tab(label="1 Mes", value="1M"),
            ],
            style={'width': '100%', 'margin':'20px', 'margin-left': '10px', 'color': '#335EFF'}
        )
    ], style={'display': 'flex'}),
    html.Div([
        dcc.Graph(id='coin-candles-graph')
    ]),
    html.P(['-------------------------------------------------------------'],style={'textAlign': 'center'}),
    html.H2(['2024 - Walter Gomez- fullstack developer'], style={ 'textAlign': 'center',"color": "#1A5276", "font-weight": "bold",'fontSize': 16}),
    html.P(['-------------------------------------------------------------'],style={'textAlign': 'center'})
], style={'background-color': '#D5D8DC', 'margin': 'auto'})


@app.callback(
    Output('coin-candles-graph', 'figure'),    
    [Input('coin-dropdown', 'value'),
     Input('tabs', 'value')]
)
def update_graph(selected_coin, selected_interval):
    data = get_binance_data(f"{selected_coin} USDT", selected_interval, 200)
    dates, popen, phigh, plow, pclose = data_extract(data)

    # Calculate technical indicators using ta
    df = pd.DataFrame({'close': pclose, 'high': phigh, 'low': plow, 'open': popen})
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close']).rsi()
    df['stoch_k'] = ta.momentum.StochasticOscillator(high=df['high'], low=df['low'], close=df['close']).stoch()
    df['stoch_d'] = ta.momentum.StochasticOscillator(high=df['high'], low=df['low'], close=df['close']).stoch_signal()

    fig = create_candles_plot(dates, popen, phigh, plow, pclose, selected_coin, rsi=df['rsi'], stoch_k=df['stoch_k'], stoch_d=df['stoch_d'])
    fig.update_layout(
        height = 800,  # Set the height as per your requirement
        #width=1200,  # Set the width as per your requirement
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
