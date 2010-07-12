'''
Created on Jul 5, 2010

@author: jbrukh
'''

#
# This is a horrible hack because of some ridiculous
# Windows-related path issues with dependency modules.
#
import sys
sys.path.append("G:\\jake\\software\\python26\\lib\\site-packages")
#
# END OF HACK
#

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from datetime import datetime

class IbPriceReader:
    
    def __init__(self, stocks, receiver, exchange='BATS', host='localhost', port=7496, client_id=0):
        """Create a new instance.
        
            stocks: a list of stock symbols
            receiver: implements a accept_tick(timestamp, symbol, price) method
            
        """
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
             
        if self.receiver != None:
            self.receiver.accept_tick( timestamp, symbol, price )    
   
        
    def start(self):
        """Start the connection and read the realtime bars for the specified 
        tickers.
        """
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
        """Cancel all the realtime bar subscriptions and disconnect.
        
        """
        for inx,stock in enumerate(self.stocks):
            print "Cancelling:\t%d = %s" % (inx,stock)
            self.connection.cancelRealTimeBars(inx)
        self.connection.disconnect()


if __name__ == '__main__':
    class Poop:
        def accept_tick(self, timestamp, symbol, price):
            print timestamp, symbol, price
            
    reader = IbPriceReader(["AAPL"], Poop())
    reader.start()
    
    raw_input("any key")