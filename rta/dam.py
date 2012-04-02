import abc
import urllib
import traceback
from operator import itemgetter
from matplotlib import finance as matplotlib_finance

from rta.model import Quote
from rta.errors import UfException, Errors

import logging
import pandas
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
        if self.symbol is None:
            LOG.debug('Symbol is None')
            return []

        return matplotlib_finance.fetch_historical_yahoo(self.symbol, start, end)
    
      
class BhavcopyDam(BaseDAM):
  ''' BhavcopyDam: used to import qoutes from NSE. '''
  
  def readQuotes(self, start, end):
    pass
  
  @classmethod
  def importFromDirectory(dir):
    if not dir:
      return
    for csv in os.listdir( os.path.abspath(dir) ):
      df = pandas.read_csv( csv, parse_dates = True, converters= { 'date': dateutil.parser.parse } )