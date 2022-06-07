//const getData = async () => {
//  const res = await fetch(context);
//  const resp = await res.text();

//  const cdata = resp.split('\n').map((row) => {
//    const [Date, Open, High, Low, Close] = row.split(',');
//    return {
//      Date: Date//(`${time1}, ${time2}`).getTime() / 1000,
//      open: Open,
//      high: High,
//      low: Low,
//      close: Close,
//    };
//  });
//  return cdata;
//
//} ;



const displayChart = async () => {
  const chartProperties = {
    width: 1500,
    height: 600,
    timeScale: {
      timeVisible: true,
      secondsVisible: true,
    },
  };

  const domElement = document.getElementById('chart');
  const chart = LightweightCharts.createChart(domElement, chartProperties);
  const candleseries = chart.addCandlestickSeries();
  const klinedata = context; //await getData();
  candleseries.setData(klinedata);
};

displayChart();
