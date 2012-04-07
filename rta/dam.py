import abc, re
from rta.api import *

# logger
import logging
LOG = logging.getLogger()


class BaseDAM(object):
    ''' base class for DAO '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        ''' constructor '''
        self.__symbol = None

    def readQuotes(self, start, end):
        ''' read quotes '''
        raise UfException(Errors.UNDEFINED_METHOD, "readQuotes method is not defined")

    def writeQuotes(self, quotes):
        ''' write quotes '''
        raise UfException(Errors.UNDEFINED_METHOD, "writeQuotes method is not defined")

    def readTicks(self, start, end):
        ''' read ticks '''
        raise UfException(Errors.UNDEFINED_METHOD, "readTicks method is not defined")

    def writeTicks(self, ticks):
        ''' read quotes '''
        raise UfException(Errors.UNDEFINED_METHOD, "writeTicks method is not defined")

    def setSymbol(self, symbol):
        ''' set symbol '''
        self.__symbol = symbol

    def __getSymbol(self):
        ''' get symbol '''
        return self.__symbol

    def setup(self, settings):
        ''' setup dam '''
        pass

    def commit(self):
        ''' commit write changes '''
        pass

    symbol = property(__getSymbol, setSymbol)


class YahooDAM(BaseDAM):
    ''' Yahoo DAM '''

    def __init__(self):
        ''' constructor '''
        super(YahooDAM, self).__init__()
        
    def readQuotes(self, start, end):
        ''' read quotes from Yahoo Financial'''
        ''' return a dataframe '''
        if self.symbol is None:
            LOG.debug('Symbol is None')
            return []

        data = pandas.read_csv( 
              matplotlib_finance.fetch_historical_yahoo(self.symbol, start, end), 
              parse_dates=True, 
              converters= { 'Date': dateutil.parser.parse } ) 
              
        return data
        
    def namespace(self, s):
      return '.ns'
      
    def importQuotes(self, importer, start, end, symbols = None):
      '''
        Imports data from yahoo finance between start and end date
        You can pass symbols or it would take defualt Config['symbols']
        It will show time to import and rows count    
      '''
      
      ''' 
				+req 
				a. Date importing can be much faster using mongodb upsert 
				b. we can insert at bulk rather than iterating each row in dataframe
				c. add better logging support
			'''
			
      if not symbols:
        symbols = Config['symbols']
      start_time, last_count, count = time.time(), 0, 0
      
      for symbol in symbols:
        self.symbol = symbol + self.namespace(symbol)
        print "Importing {s} between {st} - {en}".format(s= symbol, st= start, en = end)
        try:
          for index, row in self.readQuotes(start, end).iterrows():
            result = importer.add( symbol, row )
            if result and result.success:
              count += 1 
          
          print '\t{list} imported. total rows: {rows}, time: {t} ms'.format(
                    list=symbol, rows= ( count - last_count), t = time.time() - start_time )
        
          last_count = count
          
        except ( urllib2.HTTPError, StopIteration ):
          LOG.warning("Error occured while downloading csv from Yahoo for " + symbol )
      