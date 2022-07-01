#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# from pandas import read_csv
# from pandas import datetime
# from matplotlib import pyplot
# # load dataset
# def parser(x):
# 	return datetime.strptime('190'+x, '%Y-%m')
# series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
# # summarize first few rows
# print(series.head())
# # line plot
# series.plot()
# pyplot.show()


# In[ ]:


# from pandas import DataFrame
# from pandas import concat
# from pandas import read_csv
# from pandas import datetime
# from sklearn.metrics import mean_squared_error
# from math import sqrt
# from matplotlib import pyplot

# # date-time parsing function for loading the dataset
# def parser(x):
# 	return datetime.strptime('190'+x, '%Y-%m')

# # convert time series into supervised learning problem
# def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
# 	n_vars = 1 if type(data) is list else data.shape[1]
# 	df = DataFrame(data)
# 	cols, names = list(), list()
# 	# input sequence (t-n, ... t-1)
# 	for i in range(n_in, 0, -1):
# 		cols.append(df.shift(i))
# 		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
# 	# forecast sequence (t, t+1, ... t+n)
# 	for i in range(0, n_out):
# 		cols.append(df.shift(-i))
# 		if i == 0:
# 			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
# 		else:
# 			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
# 	# put it all together
# 	agg = concat(cols, axis=1)
# 	agg.columns = names
# 	# drop rows with NaN values
# 	if dropnan:
# 		agg.dropna(inplace=True)
# 	return agg

# # transform series into train and test sets for supervised learning
# def prepare_data(series, n_test, n_lag, n_seq):
# 	# extract raw values
# 	raw_values = series.values
# 	raw_values = raw_values.reshape(len(raw_values), 1)
# 	# transform into supervised learning problem X, y
# 	supervised = series_to_supervised(raw_values, n_lag, n_seq)
# 	supervised_values = supervised.values
# 	# split into train and test sets
# 	train, test = supervised_values[0:-n_test], supervised_values[-n_test:]
# 	return train, test

# # make a persistence forecast
# def persistence(last_ob, n_seq):
# 	return [last_ob for i in range(n_seq)]

# # evaluate the persistence model
# def make_forecasts(train, test, n_lag, n_seq):
# 	forecasts = list()
# 	for i in range(len(test)):
# 		X, y = test[i, 0:n_lag], test[i, n_lag:]
# 		# make forecast
# 		forecast = persistence(X[-1], n_seq)
# 		# store the forecast
# 		forecasts.append(forecast)
# 	return forecasts

# # evaluate the RMSE for each forecast time step
# def evaluate_forecasts(test, forecasts, n_lag, n_seq):
# 	for i in range(n_seq):
# 		actual = test[:,(n_lag+i)]
# 		predicted = [forecast[i] for forecast in forecasts]
# 		rmse = sqrt(mean_squared_error(actual, predicted))
# 		print('t+%d RMSE: %f' % ((i+1), rmse))

# # plot the forecasts in the context of the original dataset
# def plot_forecasts(series, forecasts, n_test):
# 	# plot the entire dataset in blue
# 	pyplot.plot(series.values)
# 	# plot the forecasts in red
# 	for i in range(len(forecasts)):
# 		off_s = len(series) - n_test + i - 1
# 		off_e = off_s + len(forecasts[i]) + 1
# 		xaxis = [x for x in range(off_s, off_e)]
# 		yaxis = [series.values[off_s]] + forecasts[i]
# 		pyplot.plot(xaxis, yaxis, color='red')
# 	# show the plot
# 	pyplot.show()

# # load dataset
# series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
# # configure
# n_lag = 1
# n_seq = 4
# n_test = 10
# # prepare data
# train, test = prepare_data(series, n_test, n_lag, n_seq)
# for item in train:
#     print("train",item)
# for item in test:
#     print("test",item)
# # make forecasts
# forecasts = make_forecasts(train, test, n_lag, n_seq)
# print("forecasts ",forecasts)
# # evaluate forecasts
# evaluate_forecasts(test, forecasts, n_lag, n_seq)
# # plot forecasts
# plot_forecasts(series, forecasts, n_test+2)


# In[ ]:


from tmgen.models import uniform_tm,spike_tm,modulated_gravity_tm,random_gravity_tm,gravity_tm,exp_tm
import csv
import os
import random


# In[ ]:


# def generate_demands(num_of_pairs):
#     number_of_time_slots=12
#     spike_mean=120
#     num_spikes=2
#     each_t_each_request_demand = {}
#     tm = spike_tm(num_of_pairs+1,num_spikes,spike_mean,number_of_time_slots)
#     for time in range(number_of_time_slots):
#         traffic = tm.at_time(time)
#         printed_pairs = []
#         user_indx = -1
#         for i in range(num_of_pairs):
#             for j in range(num_of_pairs):
#                 if i!=j:
#                     if (i,j) not in printed_pairs and (j,i) not in printed_pairs:
#                         printed_pairs.append((i,j))
#                         printed_pairs.append((j,i))
#                         user_indx+=1
#                         demand = max(1,traffic[i][j])
#                         try:
#                             each_t_each_request_demand[time][user_indx] = demand
#                         except:
#                             each_t_each_request_demand[time] = {}
#                             each_t_each_request_demand[time][user_indx] = demand
#     #print("each_t_each_request_demand",each_t_each_request_demand)
#     return each_t_each_request_demand
# each_user_pair_demands_file={0:"user_pair_demands0.csv",
#                             1:"user_pair_demands1.csv",
#                             2:"user_pair_demands2.csv"}
# for i in range(3):
#     with open(each_user_pair_demands_file[i], 'a') as newFile:                                
#         newFileWriter = csv.writer(newFile)
#         newFileWriter.writerow(["Time","Demand"]) 
# for exp in range(1,10):
#     each_t_each_request_demand = generate_demands(3)
#     for i in range(3):
#         for time in range(1,13):
#             if time<10:
#                 label = str(exp)+"-0"+str(time)
#             else:
#                 label = str(exp)+"-"+str(time)
#             demand = each_t_each_request_demand[time-1][i]
#             with open(each_user_pair_demands_file[i], 'a') as newFile:                                
#                 newFileWriter = csv.writer(newFile)
#                 newFileWriter.writerow([label,demand]) 
#     import pdb
#     #pdb.set_trace()


# In[ ]:





# In[ ]:


from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
from pandas import datetime
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from math import sqrt
from matplotlib import pyplot
from numpy import array
import csv
# date-time parsing function for loading the dataset
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')

# convert time series into supervised learning problem
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
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
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

# create a differenced series
def difference(dataset, interval=1):
	diff = list()
	for i in range(interval, len(dataset)):
		value = dataset[i] - dataset[i - interval]
		diff.append(value)
	return Series(diff)

# transform series into train and test sets for supervised learning
def prepare_data(series, n_test, n_lag, n_seq):
	# extract raw values
	raw_values = series.values
	# transform data to be stationary
	diff_series = difference(raw_values, 1)
	diff_values = diff_series.values
	diff_values = diff_values.reshape(len(diff_values), 1)
	# rescale values to -1, 1
	scaler = MinMaxScaler(feature_range=(-1, 1))
	scaled_values = scaler.fit_transform(diff_values)
	scaled_values = scaled_values.reshape(len(scaled_values), 1)
	# transform into supervised learning problem X, y
	supervised = series_to_supervised(scaled_values, n_lag, n_seq)
	supervised_values = supervised.values
	# split into train and test sets
	train, test = supervised_values[0:-n_test], supervised_values[-n_test:]
	return scaler, train, test

# fit an LSTM network to training data
def fit_lstm(train, n_lag, n_seq, n_batch, nb_epoch, n_neurons):
	# reshape training into [samples, timesteps, features]
	X, y = train[:, 0:n_lag], train[:, n_lag:]
	X = X.reshape(X.shape[0], 1, X.shape[1])
	# design network
	model = Sequential()
	model.add(LSTM(n_neurons, batch_input_shape=(n_batch, X.shape[1], X.shape[2]), stateful=True))
	model.add(Dense(y.shape[1]))
	model.compile(loss='mean_squared_error', optimizer='adam')
	# fit network
	for i in range(nb_epoch):
		model.fit(X, y, epochs=1, batch_size=n_batch, verbose=0, shuffle=False)
		model.reset_states()
	return model

# make one forecast with an LSTM,
def forecast_lstm(model, X, n_batch):
	# reshape input pattern to [samples, timesteps, features]
	X = X.reshape(1, 1, len(X))
	# make forecast
	forecast = model.predict(X, batch_size=n_batch)
	# convert to array
	return [x for x in forecast[0, :]]

# evaluate the persistence model
def make_forecasts(model, n_batch, train, test, n_lag, n_seq):
	forecasts = list()
	for i in range(len(test)):
		X, y = test[i, 0:n_lag], test[i, n_lag:]
		# make forecast
		forecast = forecast_lstm(model, X, n_batch)
		# store the forecast
		forecasts.append(forecast)
	return forecasts

# invert differenced forecast
def inverse_difference(last_ob, forecast):
	# invert first forecast
	inverted = list()
	inverted.append(forecast[0] + last_ob)
	# propagate difference forecast using inverted first value
	for i in range(1, len(forecast)):
		inverted.append(forecast[i] + inverted[i-1])
	return inverted

# inverse data transform on forecasts
def inverse_transform(series, forecasts, scaler, n_test):
	inverted = list()
	for i in range(len(forecasts)):
		# create array from forecast
		forecast = array(forecasts[i])
		forecast = forecast.reshape(1, len(forecast))
		# invert scaling
		inv_scale = scaler.inverse_transform(forecast)
		inv_scale = inv_scale[0, :]
		# invert differencing
		index = len(series) - n_test + i - 1
		last_ob = series.values[index]
		inv_diff = inverse_difference(last_ob, inv_scale)
		# store
		inverted.append(inv_diff)
	return inverted

# evaluate the RMSE for each forecast time step
def evaluate_forecasts(test, forecasts, n_lag, n_seq):
	for i in range(n_seq):
		actual = [row[i] for row in test]
		predicted = [forecast[i] for forecast in forecasts]
		rmse = sqrt(mean_squared_error(actual, predicted))
		print('t+%d RMSE: %f' % ((i+1), rmse))

# plot the forecasts in the context of the original dataset
def plot_forecasts(series, forecasts, n_test):
	# plot the entire dataset in blue
	pyplot.plot(series.values)
	# plot the forecasts in red
	for i in range(len(forecasts)):
		off_s = len(series) - n_test + i - 1
		off_e = off_s + len(forecasts[i]) + 1
		xaxis = [x for x in range(off_s, off_e)]
		yaxis = [series.values[off_s]] + forecasts[i]
		pyplot.plot(xaxis, yaxis, color='red')
	# show the plot
	pyplot.show()

# load dataset
# series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

# configure

# make forecasts
def forcast_demands(prediction_window,t):
    
    series = read_csv('user_pair_demands0.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

    n_lag = 1
    n_seq = 3
    n_test = 1
    n_epochs = 1500
    n_batch = 1
    n_neurons = 1
    # prepare data
    scaler, train, test = prepare_data(series, n_test, t, prediction_window)
    #print(train)
    # fit model
    model = fit_lstm(train, t, prediction_window, n_batch, n_epochs, n_neurons)
    
    
    
    
    forecasts = make_forecasts(model, n_batch, train, test, t, prediction_window)
    print("actual forcases",forecasts)
    # inverse transform forecasts and test
    forecasts = inverse_transform(series, forecasts, scaler, n_test+2)
    #actual = [row[n_lag:] for row in test]
    #actual = inverse_transform(series, actual, scaler, n_test+2)
    # evaluate forecasts
    #evaluate_forecasts(actual, forecasts, n_lag, prediction_window)
    # plot forecasts
    #plot_forecasts(series, forecasts, n_test+2)
    return forecasts
each_user_pair_predicted_demands_file = {0:"each_user_pair_predicted_demands_file0.csv",
                                         1:"each_user_pair_predicted_demands_file1.csv",
                                         2:"each_user_pair_predicted_demands_file2.csv"}
for user_pair_indx in range(2,3):
    for exp in range(100):
        for prediction_window in [2,4,6,8,10,12]:
            
            for t in range(1,13):
                #print("for time ",t)
                forecasts = forcast_demands(prediction_window,t)
                modified_forecasts = []
                for predicted in forecasts:
                    for value in predicted:
                        modified_forecasts.append(max(1,value))
                #print("forecasts",forecasts)
                with open(each_user_pair_predicted_demands_file[user_pair_indx], 'a') as newFile:                                
                    newFileWriter = csv.writer(newFile)
                    
                    my_list = ["Topology",exp,user_pair_indx,t,prediction_window]
                    for item in modified_forecasts:
                        my_list.append(item)
                    with open(each_user_pair_predicted_demands_file[user_pair_indx],'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(my_list)
    print("user_pair_indx %s for exp %s "%(user_pair_indx,exp))
print("done!")                    


# In[ ]:





# In[ ]:




