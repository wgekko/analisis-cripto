# usando ploty

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_candles_plot(dates, popen, phigh, plow, pclose, coin, rsi=None, stoch_k=None, stoch_d=None):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=['Velas', 'RSI', 'Stochastic'])

    # Add Candlestick chart
    fig.add_trace(go.Candlestick(x=dates, open=popen, high=phigh, low=plow, close=pclose, name='Velas'), row=1, col=1)

    # Add RSI trace
    if rsi is not None:
        fig.add_trace(go.Scatter(x=dates, y=rsi, mode='lines', name='RSI'), row=2, col=1)

    # Add Stochastic traces
    if stoch_k is not None and stoch_d is not None:
        fig.add_trace(go.Scatter(x=dates, y=stoch_k, mode='lines', name='Stochastic K'), row=3, col=1)
        fig.add_trace(go.Scatter(x=dates, y=stoch_d, mode='lines', name='Stochastic D'), row=3, col=1)

    fig.update_layout(
        title_text=f"{coin} - Evolución Valores",
        xaxis_rangeslider_visible=False,
        template='plotly_dark'
    )
    return fig