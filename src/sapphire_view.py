'''
Created on Jul 7, 2010

@author: Administrator
'''

import matplotlib
matplotlib.use('TkAgg')

import numpy as np

from matplotlib.pyplot import figure, plot, show, rc, title, plot_date, draw, subplot
from matplotlib.ticker import ScalarFormatter, MultipleLocator
from ib_price_reader import IbPriceReader
from time import sleep
import pickle
import sys
import threading
from threading import RLock
from math import sqrt, ceil

PERSISTENCE_FILE='sapphire-view.ser'

class SapphireView:
    
    def __init__(self, symbols, depersist=True, range_lookback=10, shocks_lookback=90, shocks_thresh=0.05):
        
        # set the fonts for matplotlib
        font = {'family' : 'monospace','size': 9}
        rc('font',**font)
        
        # init
        self.symbols = symbols
        self.price_data = self.init_price_data(symbols,depersist)
        self.started = False
        self.lock = RLock()
    
        # strategy parameters
        self.range_lookback = range_lookback
        self.shocks_lookback = shocks_lookback
        self.shocks_thresh = shocks_thresh
    
    def init_price_data(self, symbols, depersist=False):
        if not depersist:
            result = {}
            for symbol in symbols:
                result[symbol] = {'timestamps':[], 'prices':[]}
            return result
        else:
            try:
                fp = open(PERSISTENCE_FILE,'r')
                data = pickle.load(fp)
                fp.close();
                
                # remove those tickers that we do not wish to trade now
                extra_symbols = set(data.keys()).difference(set(self.symbols))
                for symbol in extra_symbols:
                    del data[symbol]
                    
                return data
            except:
                print "Could not depersist (resetting...)"
                return self.init_price_data(symbols)
    
    def accept_tick(self, timestamp, symbol, price):
        with self.lock:
            # get the price data for this symbol
            store = self.price_data[symbol]
            id = self.symbols.index(symbol)

            # get the data
            timestamps = store['timestamps']
            timestamps.append(timestamp)
            prices = store['prices']
            prices.append( np.around(price,2) )
    
            # save the data
            self.persist()
      
            if self.started:
                self.plot_price_data(id,symbol,timestamps,prices)
    
    def persist(self):
        with self.lock:
            try:
                fp = open(PERSISTENCE_FILE,'w')
                pickle.dump(self.price_data,fp)
                fp.close()
            except:
                print "Could not persist.", sys.exc_info()[0]
    
    def plot_price_data(self, id, symbol, timestamps, prices):
        #print id, symbol, timestamps, prices
        
        # get the figure and axes
        #self.fig.gca()
        axes = self.plots[id]
        # clear them
        axes.clear()
        
        # plot the whole thing -- TODO: may be made more efficient?
        axes.plot_date(timestamps, prices, '-', color='black', linewidth=.5, axes=axes)
 
        # plot the minute bars
        
 
        # labeling
        axes.set_title("%s -- %s -- $%.2f" % (symbol,timestamps[-1],prices[-1]))
        axes.set_ylabel("Price")
        axes.set_xlabel("Time")
        self.fig.autofmt_xdate()
        
        # redraw
        draw()
    
    def start(self):
        self.feed = IbPriceReader(self.symbols, self, client_id=101)
       
        
        self.formatter = ScalarFormatter(useOffset=False)
        self.locator = MultipleLocator(base=0.01)
        
        rows,cols = self.get_plot_dim(len(self.symbols))
        self.fig = figure()
        #self.fig.subplots_adjust(bottom=.8)
        self.plots = []

        for inx,symbol in enumerate(self.symbols):
            axes = self.fig.add_subplot( rows, cols, inx+1)
            axes.yaxis.set_major_formatter(self.formatter)
            axes.yaxis.set_major_locator(self.locator)
            
            self.plots.append(axes)
        
        self.started = True
        def async_start():
            print "Starting feed in 5 secs..."
            sleep(5)
            self.feed.start()
        thr = threading.Thread(target=async_start)
        thr.start()
        
        show()
    
    def get_plot_dim(self, n):
        if n == 1:
            return (1,1)
        side = int(ceil(sqrt(n)))
        slots = side**2
        if slots-n >= side:
            return (side,side-1)
        return (side,side)
    
    def stop(self):
        self.feed.stop()

if __name__ == '__main__':
    view = SapphireView(['MRK', 'QCOM', 'BP', 'JPM'], depersist=True)
    view.start()