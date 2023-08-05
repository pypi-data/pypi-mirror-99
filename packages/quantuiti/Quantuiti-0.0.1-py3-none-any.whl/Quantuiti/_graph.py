# import required packages 
import matplotlib.pyplot as plt 
from mplfinance.original_flavor import candlestick2_ohlc
import pandas as pd 
import matplotlib.dates as mpdates 
import datetime
from time import sleep
def graph(self):
    df = self.data[['Open', 'High', 'Low', 'Close']]
    fig, ax = plt.subplots()
    df.index = df.index.to_pydatetime()
    candlestick2_ohlc(ax, df['Open'], df['High'], df['Low'], df['Close'], width=0.6, colordown='red', colorup='green')
    


    plt.show()