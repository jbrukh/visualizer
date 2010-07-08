'''
Created on Jul 7, 2010

@author: Administrator
'''

from ib_price_reader import IbPriceReader
from time import sleep

import matplotlib
#matplotlib.use('TkAgg')

from matplotlib.pyplot import *
from matplotlib.ticker import ScalarFormatter

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
        prices = np.around(store['prices'],2)
       	timestamps = store['timestamps']
        self.plot_price_data(timestamps,prices)
    
    def plot_price_data(self, timestamps, prices):
		self.axes.clear()
		
		# plot
		self.axes.plot_date(timestamps, prices, '-', color='black', linewidth=.5 )
		self.fig.autofmt_xdate()
		# redraw draw the canvas
		self.fig.canvas.draw()
    
    def start(self):
        self.feed = IbPriceReader(self.symbols, self)
        self.feed.start()
        
        self.fig = figure()
        self.axes = self.fig.add_subplot(111)
        formatter = ScalarFormatter(useOffset=False)
        self.axes.yaxis.set_major_formatter(formatter)
        
        self.started = True
        show()
    
    def stop(self):
        self.feed.stop()

if __name__ == '__main__':
    view = SapphireView(['MRK'])
    view.start()