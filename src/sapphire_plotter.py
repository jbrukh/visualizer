'''
Created on Jul 12, 2010

@author: Administrator
'''
import matplotlib
matplotlib.use('WxAgg')
import numpy as np
import sys
import csv
import time

from matplotlib.pyplot import figure, plot, show, rc, title, plot_date, draw, subplot


def main(lime_file,symbol_file):
    plot_symbol(symbol_file)
    
def plot_symbol(symbol_file):
    
    # open and read the file
    
    fp = open(symbol_file,'r')
    rows = csv.reader(fp)
    
    rows.next()
    
    timestamps = []
    for row in rows:
        time_str = row[3] + ' ' + row[4]
        timestamp = time.strptime(time_str, "%m/%d/%Y %H:%M:%S")
        timestamps.append(timestamp)
        
    
    fig = figure()
    axes = fig.add_subplot()
    
    

def usage():
    print
"""USAGE: sapphire_plotter.py [lime_file] [symbol_file]""" 

if __name__ == '__main__':
    try:
        lime_file = sys.argv[1]
        symbol_file = sys.argv[2]
    except:
        usage()
        sys.exit(2)
        
    main(lime_file, symbol_file)
    show()