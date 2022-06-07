# import yfinance as yf
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# #import pandas_datareader as data
# from sklearn.preprocessing import MinMaxScaler
# from keras.models import load_model
# import mplfinance as mpl
#
# # model=load_model('..\keras_model.h5')
# model = load_model('keras2_model.h5')
# # model2 = load_model('lstm_model.h5')
# hist=yf.Ticker('SBIN.NS')
# df=hist.history(period='max',auto_adjust="True")
#
#
# df.info()
#
# df=df.reset_index()
# df.head()
#
# df=df.drop(['Dividends','Stock Splits'],axis=1)
# df.head()
# df=df.reset_index()
# # ma100=df.Close.rolling(100).mean()
# # print(ma100)
#
# # plt.figure(figsize=(12,6))
# # plt.plot(df.Close)
# # plt.plot(ma100,'r')
# # plt.show()
#
#
# # ma200=df.Close.rolling(200).mean()
# # print(ma200)
#
#
# # plt.figure(figsize=(16,8))
# # plt.plot(df.Close)
# # plt.plot(ma100,'r')
# # plt.plot(ma200,'g')
#
# # print(df.shape)
#
#
# data_training=pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
# data_testing=pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])
#
# # print(data_training.shape)
# # print(data_testing.shape)
#
# scaler=MinMaxScaler(feature_range=(0,1))
#
# data_training_array=scaler.fit_transform(data_training)
# # print(data_training_array)
#
#
# # print(data_training_array.shape)
#
# x_train = []
# y_train = []
#
# for i in range(100, data_training_array.shape[0]):
#     x_train.append(data_training_array[i - 100: i])
#     y_train.append(data_training_array[i, 0])
#
# x_train, y_train = np.array(x_train), np.array(y_train)
#
# # print(x_train.shape)
#
#
#
# past_100_days=data_training.tail(100)
#
# final_df=past_100_days.append(data_testing,ignore_index=True)
#
# input_data=scaler.fit_transform(final_df)
# # input_data
#
# x_test=[]
# y_test=[]
#
# for i in range(100,input_data.shape[0]):
#   x_test.append(input_data[i-100:i])
#   y_test.append(input_data[i,0])
#
#
# x_test,y_test=np.array(x_test),np.array(y_test)
# # print(x_test.shape)
# # print(y_test.shape)
#
#
# y_predicted = model.predict(x_test)
#
#
# # y_predicted.shape
#
# scale_factor=1/0.00622011
# y_predicted=y_predicted*scale_factor
#
# y_test=y_test*scale_factor
#
# plt.figure(figsize=(12,6))
# plt.plot(y_test,'b',label='original price')
# plt.plot(y_predicted,'r',label='predicted price')
# plt.xlabel('Time')
# plt.ylabel('price')
# #pf=plt.show()
#
#
