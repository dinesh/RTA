
import json
from collections import namedtuple
import tables

from rta.configuration import config

QUOTE_FIELDS = ['date', 'open', 'high', 'low', 'close', 'volume', 'adj']

class Quote( tables.IsDescription ):
    ''' tick class '''
    date     = tables.Time32Col()
    open     = tables.FloatCol()
    high     = tables.FloatCol()
    low      = tables.FloatCol()
    volume   = tables.UInt32Col()
    adj      = tables.FloatCol()
    
    def __str__(self):
        ''' convert to string '''
        return json.dumps({"time": self.date,
                           "open": self.open,
                           "high": self.high,
                           "low": self.low,
                           "close": self.close,
                           "volume": self.volume,
                           "adj": self.adj})

    @staticmethod
    def fromStr(string):
        ''' convert from string'''
        d = json.loads(string)
        return Quote(d['date'], d['open'], d['high'],
                     d['low'], d['close'], d['volume'], d['adj'])
  
class Database(object):
  
  def __init__(self):
    pass
    
  def setup(self):
    file = tables.openFile( config['dbpath'], 'a')
    group = file.createGroup(file.root, 'nse_eod')
    
    # for symbol in config['symbols']:
    file.createTable( group, 'symnol', Quote)
      
  def add(self, series):
    pass
    
  