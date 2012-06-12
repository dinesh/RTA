
import json, datetime, sys
from collections import namedtuple
from pymongo.objectid import ObjectId
import mongokit, pandas

from configuration import Config
from errors import Errors, UfException



REQUIRED_QUOTE_FIELDS = ['symbol', 'tick', 'open', 'high', 'low', 'close', 'volume']

class Quote( mongokit.Document ):
    ''' qoute class '''
    structure = { 
        'symbol': basestring,
        'tick' : datetime.datetime, 
        'high': float,
        'close': float,
        'adj': float,
        'open' : float,
        'low': float, 
        'volume': long,
    }
    
    required_fields = REQUIRED_QUOTE_FIELDS
    
    indexes = [ { 
        'fields': ['symbol', 'tick'],
        'unique'  : True 
      } ]
      
    @classmethod
    def scope(_cls):
     return MongoDB().collection()
     
    def __repr__(self):
        ''' convert to string '''
        return json.dumps({"tick": self.tick,
                           "open": self.open,
                           "high": self.high,
                           "low": self.low,
                           "close": self.close,
                           "volume": self.volume,
                           "symbol": self.symbol })
    
    # IMP: add caching behaviour some decorater stuff 
    @classmethod
    def series(_cls, symbol, start=None, end=None, frame=True, **kwgs):
      '''
        The function returns dataframe with all of the field ( _repr_ fields )
        You can have the series out of dataframe by 
          >> Quote.series( symbol = '3MINDIA' )
          >> Quote.series( symbol = '3MINDIA' )['close']
        
      '''
      print start, end
      
      try:
        mongo = MongoDB().collection()
        cursor = None
        if not end:
          end = datetime.datetime.today()
        
        cursor = mongo.find( { 
                  'symbol': symbol, 
                  'tick': { '$gte' : start, '$lte' : end } 
                 }, fields = REQUIRED_QUOTE_FIELDS ).sort('tick')
        
        return pandas.DataFrame( list(cursor), index = [ x['tick'] for x in cursor.rewind() ] ) 
          
      except:
        raise
        raise UfException( Errors.DB_EXECUTE, sys.exc_info()[0] )
        
      

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

def db():
  return MongoDB()
  
  
@singleton
class MongoDB(object):
  def __init__(self, mode = 'a'):
    self.__collection = self.__connection = None
    self.col = self.collection()
    mongo_index = self.col.Quote.generate_index(self.col.Quote.collection)
  
  
  def reset(self):
    self.__collection.drop_database( DB_NAME )
    self.collection()
    
  def collection(self):
    if not self.__collection:
      if not self.__connection:
        self.__connection = mongokit.Connection()
        self.__connection.register([ Quote ])
        
      self.__collection = self.__connection[DB_NAME][COL_NAME]
    
    return self.__collection
      
  def add(self, symbol, series, force = False):
      '''TODO: This thing can be done in more efficient way. read momngokit.insert '''
     
      if not force:
        row = self.col.find_one({ 'symbol': symbol, 'tick': series['Date'] } )
        if not row:
          return self.insert(symbol, series)
      else:
        return self.insert(symbol, series)
                  
  def insert(self, symbol, series):
    _quote = self.col.Quote
    data =  { 'symbol': symbol, 
             'tick': series['Date'], 
             'open': series['Open'],
             'high': series['High'], 
             'low': series['Low'],
             'adj': series['Adj Close'], 
             'close': series['Close'],
             'volume': long(series['Volume'])
          }
    doc = self.col.Quote( data )
    doc.save(validate=True)
    tp = namedtuple('quote_result', ['success', 'doc'] )
    if isinstance( doc['_id'], ObjectId ):
      return tp( True, doc)
    else:
      return tp( False, None )

  
