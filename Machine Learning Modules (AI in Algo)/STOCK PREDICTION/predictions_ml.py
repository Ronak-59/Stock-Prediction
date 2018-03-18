import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import LSTM
import time
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1
	df = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

# transform series into train and test sets for supervised learning
def prepare_data(series, n_test, n_lag, n_seq):
	# extract raw values
	raw_values = series
	raw_values = raw_values.reshape(len(raw_values), 1)
	# transform into supervised learning problem X, y
	supervised = series_to_supervised(raw_values, n_lag, n_seq)
	supervised_values = supervised.values
	# split into train and test sets
	train, test = supervised_values[0:-n_test], supervised_values[-n_test:]
	return train, test

def persistence(last_ob, n_seq):
	return [last_ob for i in range(n_seq)]

def make_forecasts(train, test, n_lag, n_seq):
	forecasts = list()
	for i in range(len(test)):
		X, y = test[i, 0:n_lag], test[i, n_lag:]
		# make forecast
		forecast = persistence(X[-1], n_seq)
		# store the forecast
		forecasts.append(forecast)
	return forecasts

# evaluate the RMSE for each forecast time step
def evaluate_forecasts(test, forecasts, n_lag, n_seq):
	for i in range(n_seq):
		actual = test[:,(n_lag+i)]
		predicted = [forecast[i] for forecast in forecasts]
		rmse = math.sqrt(mean_squared_error(actual, predicted))
# 		print('t+%d RMSE: %f' % ((i+1), rmse))

def plot_forecasts(series, forecasts, n_test):
	# plot the entire dataset in blue
	plt.plot(series)
	# plot the forecasts in red
	for i in range(len(forecasts)):
		off_s = len(series) - n_test + i - 1
		off_e = off_s + len(forecasts[i]) + 1
		xaxis = [x for x in range(off_s, off_e)]
		yaxis = [series[off_s]] + forecasts[i]
		plt.plot(xaxis, yaxis, color='red')
	# show the plot
	plt.show()

def returnArray():
    n_lag = 1
    n_seq = 15
    n_test = 15
    forecast_array = []
    filenames = np.array(['AAPL','AXP','BA','CAT','CSCO','CVX','DIS','DWDP','GE','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','TRV','UNH','UTX','V','VZ','WMT','XOM'])
    for i in range(30):
        df = pd.read_csv('data/'+filenames[i]+'.csv')
        data=df.iloc[:,-2].values
        # prepare datas
        train, test = prepare_data(data, n_test, n_lag, n_seq)
        # make forecasts
        forecasts = make_forecasts(train, test, n_lag, n_seq)
        # evaluate forecasts
        evaluate_forecasts(test, forecasts, n_lag, n_seq)
        # plot forecasts
    #     plot_forecasts(data, forecasts, n_test+2)
        forecast_array.append(((forecasts[14][0]-forecasts[0][0])/forecasts[0][0]))
    mini = min(forecast_array)
    maxi = max(forecast_array)
    for i in range(30):
        forecast_array[i] = ((forecast_array[i]+abs(mini))/(maxi-mini))
        forecast_array[i] = round(forecast_array[i]*10,2)
    return forecast_array


print(returnArray())