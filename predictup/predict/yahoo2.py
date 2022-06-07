import yfinance as yf
import numpy as np
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from .graph import get_plot
from django.shortcuts import render
import base64
from io import BytesIO
from .forms import Predict
from django.shortcuts import render, HttpResponseRedirect

# def dash(request):
#     nm = request.fname
#     dashboard(request,nm)


def dashboard(request,my_name):
    #############################################################
    # search = Predict(request.POST)
    # if search.is_valid():
    #     nm = search.cleaned_data['search']
    #     return HttpResponseRedirect('/dashboard2/nm/')

    # search = Predict()
    print(my_name)
    model = load_model('model_krishnaik06.h5')
    hist = yf.Ticker(my_name)
    df = hist.history(period='max', auto_adjust="True")

    df1 = df.reset_index()['Close']
    current_price = df1.tail(1)
    current_price=df['Close'].iloc[-1]

    # plt.plot(df1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    df1 = scaler.fit_transform(np.array(df1).reshape(-1, 1))

    ##splitting dataset into train and test split
    training_size = int(len(df1) * 0.65)
    test_size = len(df1) - training_size
    train_data, test_data = df1[0:training_size, :], df1[training_size:len(df1), :1]

    # training_size,test_size

    # convert an array of values into a dataset matrix
    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]  ###i=0, 0,1,2,3-----99   100
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return numpy.array(dataX), numpy.array(dataY)

    # reshape into X=t,t+1,t+2,t+3 and Y=t+4
    time_step = 100
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, ytest = create_dataset(test_data, time_step)

    # reshape input to be [samples, time steps, features] which is required for LSTM
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    ### Create the Stacked LSTM model
    # from tensorflow.keras.models import Sequential
    # from tensorflow.keras.layers import Dense
    # from tensorflow.keras.layers import LSTM

    # model=Sequential()
    # model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
    # model.add(LSTM(50,return_sequences=True))
    # model.add(LSTM(50))
    # model.add(Dense(1))
    # model.compile(loss='mean_squared_error',optimizer='adam')

    # model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=100,batch_size=64,verbose=1)

    ### Lets Do the prediction and check performance metrics
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    ##Transformback to original form
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)

    ### Calculate RMSE performance metrics
    import math
    from sklearn.metrics import mean_squared_error

    math.sqrt(mean_squared_error(y_train, train_predict))

    ### Test Data RMSE
    math.sqrt(mean_squared_error(ytest, test_predict))

    ### Plotting
    # shift train predictions for plotting
    look_back = 100
    trainPredictPlot = numpy.empty_like(df1)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict
    # shift test predictions for plotting
    testPredictPlot = numpy.empty_like(df1)
    testPredictPlot[:, :] = numpy.nan
    testPredictPlot[len(train_predict) + (look_back * 2) + 1:len(df1) - 1, :] = test_predict

    # plot baseline and predictions
    # plt.plot(scaler.inverse_transform(df1))
    # plt.plot(trainPredictPlot)
    # plt.plot(testPredictPlot)
    # plt.show()

    a = len(test_data)
    a = a - 100

    x_input = test_data[a:].reshape(1, -1)

    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()

    # demonstrate prediction for next 10 days
    lst_output = []
    n_steps = 100
    i = 0
    while (i < 30):
        if (len(temp_input) > 100):
            # print(temp_input)
            x_input = np.array(temp_input[1:])
            # print("{} day input {}".format(i, x_input))
            x_input = x_input.reshape(1, -1)
            x_input = x_input.reshape((1, n_steps, 1))
            # print(x_input)
            yhat = model.predict(x_input, verbose=0)
            # print("{} day output {}".format(i, yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input = temp_input[1:]
            # print(temp_input)
            lst_output.extend(yhat.tolist())
            i = i + 1
        else:
            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            # print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            # print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i = i + 1

    day_new = np.arange(1, 101)
    day_pred = np.arange(101, 131)

    b = len(df1)
    b = b - 100

    aa = scaler.inverse_transform(df1[b:])
    bb = scaler.inverse_transform(lst_output)

    plt.plot(day_new, scaler.inverse_transform(df1[b:]))
    plt.plot(day_pred, scaler.inverse_transform(lst_output))

    ##############################################################

    chart = get_plot(request,day_new,day_pred,aa,bb)
    return render(request, 'predict/chart2.html',{'chart':chart,'my_name':my_name,'current_price':current_price})

def get_graph(request):
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    # print(image_png)
    graph = base64.b64encode(image_png)
    # print(graph)
    graph = graph.decode('utf-8')
    # print(graph)
    buffer.close()
    return graph

def get_plot(request,day_new,day_pred,aa,bb):
    plt.figure(figsize=(12, 6))
    plt.plot(day_new, aa, 'b', label='original price')
    plt.plot(day_pred, bb, 'r', label='predicted price')
    plt.xlabel('Time')
    plt.ylabel('price')

    graph = get_graph(request)
    return graph