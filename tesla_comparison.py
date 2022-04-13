from DEF_MFS_MVP_Storage import df_list
import pandas as pd
import plotly.graph_objects as go

def rolling_50():
    data = pd.concat(df_list)
    data = data[data.ticker.isin(['TSLA'])]
    data['MA50'] = data['Open'].rolling(50).mean()
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['MA50'],
                                             close=data['Close'])])
    return fig


rolling_50()