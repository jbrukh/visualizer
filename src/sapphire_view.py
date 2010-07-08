'''
Created on Jul 7, 2010

@author: Administrator
'''

from ib_price_reader import IbPriceReader
from time import sleep

import matplotlib
#matplotlib.use('TkAgg')

from matplotlib.pyplot import *

class SapphireView:
    
    def __init__(self, symbols):
        self.symbols = symbols
        self.price_data = self.init_price_data(symbols)
        self.started = False

    
    def init_price_data(self, symbols):
        result = {}
        for symbol in symbols:
            result[symbol] = {'timestamps':[], 'prices':[]}
        return result
    
    def accept_tick(self, timestamp, symbol, price):
        store = self.price_data[symbol]
        store['timestamps'].append(timestamp)
        store['prices'].append(price)
        
        if self.started:
            self.update_subplot(symbol)
   
    def update_subplot(self, symbol):
        store = self.price_data[symbol]
        
        self.axes.clear()
        prices = np.around(store['prices'],2)
        print prices
        self.axes.plot_date(store['timestamps'], prices, '-', color='black', linewidth=.5 )
        self.fig.autofmt_xdate()
        
        print np.arange(min(prices), max(prices),0.01)
        self.axes.set_yticks(np.arange(min(prices), max(prices),0.01))
        
        # draw
        self.fig.canvas.draw()
             
    def start(self):
        self.feed = IbPriceReader(self.symbols, self)
        self.feed.start()
        
        self.fig = figure()
        self.fig.subplots_adjust(left=0.2)
        self.axes = self.fig.add_subplot(111)
        
        formatter = matplotlib.ticker.MultipleLocator(base=0.01)        
        
        self.started = True
        show()
        
    def stop(self):
        self.feed.stop()
        
if __name__ == '__main__':
    view = SapphireView(['MRK'])
    view.start()