
import json, datetime
from collections import namedtuple
from pymongo.objectid import ObjectId
import mongokit

from .configuration import Config

REQUIRED_QUOTE_FIELDS = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']

class Quote( mongokit.Document ):
    ''' qoute class '''
    structure = { 
        'symbol': basestring,
        'date' : datetime.datetime, 
        'high': float,
        'close': float,
        'adj': float,
        'open' : float,
        'low': float, 
        'volume': int,
    }
    
    required_fields = REQUIRED_QUOTE_FIELDS
    
    indexes = [ { 
        'fields': ['symbol', 'date'],
        'unique'  : True 
      } ]
    
    def __repr__(self):
        ''' convert to string '''
        return json.dumps({"date": self.date,
                           "open": self.open,
                           "high": self.high,
                           "low": self.low,
                           "close": self.close,
                           "volume": self.volume,
                           "symbol": self.symbol })



def singleton(class_):
 instances = {}
 def getinstance(*args, **kwargs):
   if class_ not in instances:
       instances[class_] = class_(*args, **kwargs)
   return instances[class_]
 return getinstance


DB_NAME = Config['dbname'] 
if not DB_NAME:
  DB_NAME =  'nse_eod'
  
COL_NAME = 'quotes'

@singleton
class MongoDB(object):
  def __init__(self, mode = 'a'):
      self._connection = mongokit.Connection()
      self.col = self._connection[DB_NAME][COL_NAME]
      self._connection.register([ Quote ])
      
      mongo_index = self.col.Quote.generate_index(self.col.Quote.collection)
      
  def add(self, symbol, series, force = False):
      '''TODO: This thing can be done in more efficient way. read momngokit.insert '''
     
      if not force:
        row = self.col.find_one({ 'symbol': symbol, 'date': series['Date'] } )
        if not row:
          return self.insert(symbol, series)
      else:
        return self.insert(symbol, series)
                  
  def insert(self, symbol, series):
    _quote = self.col.Quote
    doc = _quote( { 'symbol': symbol, 
             'date': series['Date'], 
             'open': series['Open'],
             'high': series['High'], 
             'low': series['Low'],
             'adj': series['Adj Close'], 
             'close': series['Close'],
             'volume': series['Volume']
          } )
          
    doc.save()
    tp = namedtuple('quote_result', ['success', 'doc'] )
    if isinstance( doc['_id'], ObjectId ):
      return tp( True, doc)
    else:
      return tp( False, None )

  