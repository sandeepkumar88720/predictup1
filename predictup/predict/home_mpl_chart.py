import pandas as pd
import mplfinance as mpl
import yfinance as yf
from django.shortcuts import render, HttpResponseRedirect
import base64
from io import BytesIO
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from .forms import Charttwo,Predict


# period=None
# interval=None

#
# def abcd(request):
#     if request.method == "POST":
#         ct=Chart(request.POST)
#         return ct
#     else:
#         fm=Chart
#         return render(request, "predict/home_mpl_char.html", {'ct': fm})
#
def get_graph(request,data):
    buffer = BytesIO()
    mpl.plot(data, type='line',style='yahoo',volume=True,  savefig=dict(fname=buffer), tight_layout=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    # print(image_png)
    graph = base64.b64encode(image_png)
    # print(graph)
    graph = graph.decode('utf-8')
    # print(graph)
    buffer.close()
    return graph

def chart_plot(request):

    hist = yf.Ticker('AAPL')
    data = hist.history(period='1y',style='yahoo',volume=True, auto_adjust="True")
    data = data.reset_index()
    data.Date = pd.to_datetime(data.Date)
    data = data.set_index('Date')
    # current_price=data.reset_index()['Close']
    # current_price=current_price.tail(1)
    chart = get_graph(request,data)
    return chart

##############################################################################

history=yf.Ticker('AAPL')
df=history.history(period="max", auto_adjust="True")
df=df.reset_index()

df.Date = pd.to_datetime(df.Date)
df = df.set_index('Date')


def graph_get(request,nm,st,vol,tp,pr,interval):
    hist = yf.Ticker(nm)
    data = hist.history(period=pr, interval=interval, auto_adjust="True")
    data = data.reset_index()
    data.Date = pd.to_datetime(data.Date)
    data = data.set_index('Date')

    buffer = BytesIO()
    mpl.plot(data, type=tp, volume=vol, style=st,savefig=dict(fname=buffer),tight_layout=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    # print(image_png)
    graph = base64.b64encode(image_png)
    # print(graph)
    graph = graph.decode('utf-8')
    # print(graph)
    buffer.close()
    return graph


# def get_plot_mpl(request,st,vol,type):
#      graph = graph_get(request,st,vol,type)
#      return graph
def home_mpl(request):
    chart = chart_plot(request)
    if request.method == "POST":
        fm = Charttwo(request.POST)
        search = Predict(request.POST)
        if search.is_valid():
            name = search.cleaned_data['search']
            print(name)
            return HttpResponseRedirect('/dashboard2/'+name)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            st = fm.cleaned_data['style']
            vol = fm.cleaned_data['volume']
            pr = fm.cleaned_data['period']
            interval= fm.cleaned_data['interval']
            tp = fm.cleaned_data['type']



            graph = graph_get(request,nm, st, vol, tp,pr,interval)
            fm = Charttwo()
            search = Predict()
            return render(request, 'predict/chart.html', {'chart': graph,'ct': fm,'nm':nm, 'search':search})
    else:
        fm = Charttwo()
        search = Predict()
        chart= chart_plot(request)
        return render(request, 'predict/chart.html',{'chart':chart,'ct': fm,'nm':'^NSEI', 'search':search})

