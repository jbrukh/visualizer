'''
Created on Jul 12, 2010

@author: Administrator
'''
import matplotlib
matplotlib.use('WxAgg')
import numpy as np
import sys
import csv
from time import strptime, strftime
from datetime import datetime

from matplotlib.pyplot import figure, plot, show, rc, title, plot_date, draw, subplot
from matplotlib.dates import date2num

class SapphirePlotter():
    
    def __init__(self, lime_file, symbol_file, symbol):
        font = {'family' : 'monospace','size': 7}
        rc('font',**font)
        self.symbol = symbol
        self.symbol_file = symbol_file
        self.lime_file = lime_file
        
    def plot(self):
        """Go on and plot the action.
        """
        self.fig = figure()
        self.axes = self.fig.add_subplot(111)
        
        # plot the prices
        self.__plot_prices()
        # plot the annotations
        self.__plot_annotations()

        show()

    def __plot_prices(self):
        """Plots the prices read in from the symbol_file.
        """
        fp = open(self.symbol_file,'r')
        reader = csv.reader(fp)
        
        
        #reader.next()
        
        timestamps = []
        closes = []
        shock_timestamps = []
        shocks = []
        cnt = 0
        for line in reader:
            cnt += 1
            print line
            
            # get the timestamp
            ts = " ".join(line[0:2])
            ts = strptime(ts, "%m/%d/%y %H:%M")
            ts = datetime(*ts[:6])
            timestamps.append(ts)
            
            close = np.around(float(line[2]),2) 
            
            if len(closes)>=10:
                lookback = closes[-10:]
                low,high = np.amin(lookback), np.amax(lookback)
                if close > high or close < low:
                    shock_timestamps.append(ts)
                    shocks.append(close)
            
            # save the close
            closes.append( close )
        
        # organize the dimensions
        low,high = np.amin(closes),np.amax(closes)
        self.rng = high-low
        if self.rng > 0:
            low,high = low-.20*self.rng, high+.20*self.rng
            self.axes.set_ylim(low,high)
        
        
        # now, plot them    
        self.axes.plot_date(timestamps, closes, '-o', 
                           color='black', 
                           linewidth=.5, markersize=2)
        self.axes.plot_date(shock_timestamps, shocks, 'o', color='red', markersize=3, markeredgecolor='red')
        title("%s %s" % (self.symbol, strftime("%Y-%m-%d",timestamps[0].timetuple())))
    
    def __plot_annotations(self):
        """Plots the annotations read in from the lime_file.
        """
        fp = open(self.lime_file,'r')
        reader = csv.reader(fp)
        reader.next()
        
        timestamps = []
        prices = []
        sides = []
        qtys = []
        leftover = 0
        for row in reader:
            if row[1]==self.symbol:
                print row
                qty = int(row[8])
                if ((qty+leftover) % 100) != 0:
                    leftover = qty+leftover
                    continue
                else:
                    qty += leftover
                    qtys.append(qty)
                    leftover = 0
                
                ts = " ".join(row[3:5])
                ts = strptime(ts, "%m/%d/%Y %H:%M:%S")
                ts = datetime(*ts[:6])
                timestamps.append(ts)
                
                prices.append( np.around(float(row[9]),3) )
                sides.append( int(row[5]) )
                
        
        cnt = 0
        for ts in timestamps:
            x = date2num(ts)
            y = prices[cnt]
            side = sides[cnt]
                
            text = "%s %d %.3f" % (self.__get_english(side), qtys[cnt], y)
            polarity = self.__get_side(side)
            x_offset=0
            y_offset=0
            if side==3:
                x_offset = -.035
                y_offset = -polarity*.12*self.rng
            elif side==2:
                x_offset = -.025
                y_offset = -polarity*.10*self.rng
            else:
                y_offset= -polarity*.10*self.rng
            self.axes.annotate(text, xy=(x,y), xytext=(x+x_offset,y+y_offset),
                               bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec=(1., .5, .5)),
                               arrowprops=dict(
                                               fc=(1.0, 0.7, 0.7), ec=(1., .5, .5),
                                               facecolor='black', 
                                               arrowstyle='wedge,tail_width=.1', 
                                               connectionstyle="angle3") )
            cnt += 1
    def __get_side(self, value):
        if value == 1:
            return 1;
        elif value == 2 or value == 3:
            return -1;
        else:
            return 0;
        
    def __get_english(self, side):
        if side == 1:
            return "B"
        elif side == 2:
            return "S"
        elif side == 3:
            return "SH"
        else:
            return "NONE"
    
def usage():
    print
"""USAGE: sapphire_plotter.py [lime_file] [symbol_file] [symbol]""" 

if __name__ == '__main__':
    try:
        lime_file = sys.argv[1]
        symbol_file = sys.argv[2]
        symbol = sys.argv[3]
    except:
        usage()
        sys.exit(2)
        
    plotter = SapphirePlotter(lime_file, symbol_file, symbol)
    plotter.plot()
    show()