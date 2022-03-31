import numpy as np
import pandas_datareader.data as web
import yfinance as yf
# yf.pdr_override()
from datetime import date, timedelta
import pandas as pd
import numpy as np

symbols = ['TSLA', 'F', 'AAPL', 'GOOG']
start = date.today() - timedelta(days=31)
now = date.today()
stock=[]
for symbol in symbols:
    df_stock = yf.download(symbol, group_by="Ticker", start=start, end=now)
    df_stock['Ticker'] = symbol
    stock.append(pd.DataFrame(df_stock))

df=pd.concat(stock)
df_tesla=(df[df['Ticker'] == 'TSLA'])
df_ford=(df[df['Ticker'] == 'F'])
df_apple=(df[df['Ticker'] == 'AAPL'])
df_goog=(df[df['Ticker'] == 'GOOG'])

# print(df_tesla['Volume'].iloc[-1])

df_tesla=df_tesla.reset_index()
print (df_tesla['Date'])
# print(df_apple)
# print(df_goog)