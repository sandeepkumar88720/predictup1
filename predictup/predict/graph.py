import matplotlib.pyplot as plt
import base64
from io import BytesIO
import mplfinance as mpl
from .import home_mpl_chart

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

def get_plot(request,x,y_test,y_predicted):
    plt.figure(figsize=(12, 6))
    plt.plot(y_test, 'b', label='original price')
    plt.plot(y_predicted, 'r', label='predicted price')
    plt.xlabel('Time')
    plt.ylabel('price')

    graph = get_graph(request)
    return graph

def get_mpl_plot(request,data):
     mpl.plot(data, type='line', volume=True, style='yahoo')
     graph = get_graph(request)
     return graph