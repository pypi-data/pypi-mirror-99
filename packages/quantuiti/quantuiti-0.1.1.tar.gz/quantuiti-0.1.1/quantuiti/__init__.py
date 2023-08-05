import inspect
import os
import pandas as pd
from pandas_datareader import data as pdr
import random
import matplotlib.pyplot as plt
from .__about__ import *
class Engine():
    """
    CompuTradeEngine helps you reliabley backtest your trading algorithms faster than ever.
    
        Parameters:
            backtest (bool): CompuTradeEngine will backtest your algorithm.
            build    (bool): CompuTradeEngine will build you algorithm in python and output it to a build directory in your current working directory.

    """
    from ._buildPython import BuildPythonFile

    from ._graph import graph

    from ._algorithm import algorithm

    from ._sma import sma

    from ._ema import ema

    from ._cci import cci

    from ._emv import emv

    from ._roc import roc

    def __init__(self, backtest=True, build=False, graph=False):
        self.constuctors()

        # next block gets the callee's working directory
        frame_info = inspect.stack()[1]
        filepath = frame_info[1]
        filename=filepath
        del frame_info
        filepath = os.path.abspath(filepath)
        filepath = filepath.replace(f'/{filename}', '')
        self.path = filepath

        self.backtest = backtest
        self.build = build
        self.graph = graph

    def constuctors(self):
        self.algorithmFunc = None
        self.interval = 'd'
        self.position = False
        self.shares = 0
        self.startBalance = 10000
        self.balance = self.startBalance
        self.trades = []
        self.sells = []

    def backtest_algorithm(self):
        symbols = ['AIV','AAPL', 'GME']
        for symbol in symbols:
            self.CurrentSymbol = symbol
            self.index=0
            self.data = pdr.get_data_yahoo(symbols=symbol, interval=self.interval, start='JAN-01-2020', end='DEC-28-2020') # iterates over symbols by symbol to backtest algorithm on symbol data
            self.close = self.data['Close']
            for index, rows in self.data.iterrows():
                self.algo(self)


                self.index+=1

            if self.shares != 0:
                profit = ( self.data['Close'][-1]*self.shares ) - ( self.trades[-1][1] * self.shares )
                self.sells.append(profit) 
                self.balance = profit + ( self.trades[-1][1] * self.shares )
                self.shares = 0

           # fig, ax = plt.subplots(nrows=2)

           # ax[0].1_title(symbol)
           # ax[0].plot(self.data['Close'])
           # ax[0].plot(self.data['ema_20'])
           # ax[0].plot(self.data['ema_100'])

           # ax[1].set_title('cci')
           # ax[1].plot(self.data['cci_20'])
            print('balance', self.balance)
            
            roi = ((self.balance - self.startBalance) / self.startBalance) * 100
            print(f'roi: %{roi}')

            self.balance = 10000
            self.shares = 0
            # plt.show()
            if self.graph:
                self.graph()
                
    
    def buy(self):
        if self.shares == 0 and self.balance > 0 :
            self.shares = self.balance / self.data['Close'][self.index]
            self.balance = 0
            self.trades.append(tuple([self.shares, self.data['Close'][self.index]])) 
    
    def sell(self):
        if self.shares != 0:
            profit = ( self.data['Close'][self.index]*self.shares ) - ( self.trades[-1][1] * self.shares )
            self.sells.append(profit) 
            self.balance = profit + ( self.trades[-1][1] * self.shares )
            self.shares = 0
    