'''
Created on Jul 5, 2010

@author: jbrukh
'''

#
# This is a horrible hack because of some ridiculous
# Windows-related path issues with dependency modules.
#
import sys
poop = ['G:\\jake\\software\\python26', 
            'G:\\jake\\software\\python26\\Lib\\idlelib', 
            'g:\\jake\\software\\python26', 
            'C:\\WINDOWS\\system32\\python26.zip', 
            'G:\\jake\\software\\python26\\DLLs', 
            'G:\\jake\\software\\python26\\lib', 
            'G:\\jake\\software\\python26\\lib\\plat-win', 
            'G:\\jake\\software\\python26\\lib\\lib-tk', 
            'G:\\jake\\software\\python26\\lib\\site-packages']
#
# END OF HACK
#

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message


from datetime import datetime
from time import sleep
import pickle

class IbPriceReader:
    
    def __init__(self, stocks, receiver, exchange='BATS', host='localhost', port=7496, client_id=0):
        
        # get the parameters
        self.stocks     = stocks
        self.receiver   = receiver
        self.exchange   = exchange
        self.host       = host
        self.port       = port
        self.client_id  = client_id
        self.hist_data  = {}
        
    
    def ticker_updated(self, msg):
        """ ticker_updated(msg) -> called when ticker price or size data has changed
        """
        
        timestamp = datetime.fromtimestamp(msg.time)
        symbol = self.stocks[msg.reqId]
        price = msg.close
            
        print timestamp, symbol, price
        
        self.save_data(timestamp,symbol,price)
        
        if self.receiver != None:
            self.receiver.accept_tick( timestamp, symbol, price )    
   
        
    def start(self):
        # connection and handler
        self.connection = ibConnection(
                                       host=self.host, 
                                       port=self.port, 
                                       clientId=self.client_id)
        
        # registration
        self.connection.register( self.ticker_updated, message.RealtimeBar )
        
        # connect
        self.connection.connect()
        
        for inx,stock in enumerate(self.stocks):
            print "Requesting:\t%d = %s" % (inx,stock)
            
            # create the contract
            contract = Contract()
            contract.m_symbol = stock
            contract.m_secType = 'STK'
            contract.m_exchange = self.exchange
            contract.m_currency = 'USD'
            
            self.connection.reqRealTimeBars(inx, contract, 5, 'TRADES', False)
            

    def stop(self):
        for inx,stock in enumerate(self.stocks):
            print "Cancelling:\t%d = %s" % (inx,stock)
            self.connection.cancelRealTimeBars(inx)
        self.connection.disconnect()
    
    def save_data(self, timestamp, symbol, price):
        if not self.hist_data.has_key(symbol):
            self.hist_data[symbol]={'timestamps':[], 'prices':[]}
        
        data = self.hist_data[symbol]
        data['timestamps'].append(timestamp)
        data['prices'].append(price)
