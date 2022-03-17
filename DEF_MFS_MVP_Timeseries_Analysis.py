
import pandas as pd
import glob
import datetime
import numpy as np
import plotly.express as px
import warnings
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

#Reading the data
df = pd.read_csv("ticker_AAPL.csv")
df = df.reset_index()
df = df.drop(['index','Adj Close'], axis=1)
df

warnings.filterwarnings('ignore')

train_data, test_data = df[0:int(len(df)*0.8)], df[int(len(df)*0.8):]

fig = px.line(df, x="Date", y="Open", color_discrete_map={"Open": "goldenrod"})
fig.add_scatter(x=train_data['Date'], y=train_data['Open'], mode='lines')
fig.show()

def smape_kun(y_true, y_pred):
    return np.mean((np.abs(y_pred - y_true) * 200/ (np.abs(y_pred) + np.abs(y_true))))

train_ar = train_data['Open'].values
test_ar = test_data['Open'].values

history = [x for x in train_ar]
print(type(history))

predictions = list()
for t in range(len(test_ar)):
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test_ar[t]
    history.append(obs)
#     print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test_ar, predictions)
print('Testing Mean Squared Error: %.3f' % error)
error2 = smape_kun(test_ar, predictions)
print('Symmetric mean absolute percentage error: %.3f' % error2)

fig = px.line(predictions, title='Stock Prices Predicted')
# fig.add_scatter(x=test_data['Date'], y = test_data['Open'], mode='lines')
fig.show()

test_data=test_data.reset_index(drop=True)
frames=[test_data,dff]
new_df=pd.concat(frames, axis=1)

fig = px.line(new_df, x="Date", y="Predicted", color_discrete_map={"Open": "goldenrod"})
fig.add_scatter(x=new_df['Date'], y = new_df['Open'], mode='lines')
# fig.add_scatter(x=test_data['Date'], y = test_data['Open'], mode='lines')
fig.show()

fc, se, conf = model_fit.forecast(51, alpha=0.05)  # 95% confidence

fc_series = pd.Series(fc, index=test_data.index)
lower_series = pd.Series(conf[:, 0], index=test_data.index)
upper_series = pd.Series(conf[:, 1], index=test_data.index)

fig = px.line(train_data, x="Date", y="Open")
fig.show()

new_df=new_df.reset_index(drop=True)
frames=[train_data, new_df]
new_dff=pd.concat(frames)
new_dff

