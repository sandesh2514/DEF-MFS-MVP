import pandas as pd
from prophet import Prophet
from DEF_MFS_MVP_Storage import df_list
from prophet.plot import plot_plotly

def ford_pred():
    data = pd.concat(df_list)
    tick = data[data.ticker.isin(['F'])]
    tick = pd.DataFrame(tick)
    tick['ds'] = tick['Date'].copy()
    tick['y'] = tick['Open'].copy()
    tick = tick.drop(['Date', 'Open', 'Volume','High','Low', 'Close', 'Adj Close', 'ticker'], axis = 1)
    m = Prophet(yearly_seasonality=True, daily_seasonality=True)
    m.fit(tick)
    future = m.make_future_dataframe(periods=120)
    forecast = m.predict(future)
    figure = plot_plotly(m, forecast)
    figure.update_yaxes(color='White')
    figure.update_xaxes(color='White')
    figure.update_layout(paper_bgcolor='#1f2c56')
    return figure


ford_pred()