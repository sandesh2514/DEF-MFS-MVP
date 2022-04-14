from DEF_MFS_MVP_Storage import df_list
import pandas as pd
import plotly.graph_objects as go

def ford_rolling_50():
    data = pd.concat(df_list)
    data = data[data.ticker.isin(['F'])]
    data['MA50'] = data['Open'].rolling(50).mean()
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'])])
    fig.update_layout(paper_bgcolor="#1f2c56")
    return fig


ford_rolling_50()