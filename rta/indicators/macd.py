

from rta.api import Indicators
from rta import common
from rta import ts as TS

from . import IndicatorBase
import numpy as np
import itertools

class MACD(IndicatorBase):
  
  # 1) should extract options, 2) call talib function 3) maketimeseries of output and return
  
  def fastperiod(self):
    return int( self.cget('fastperiod') )
  
  def slowperiod(self):
    return int( self.cget('slowperiod') )
  
  def signalperiod(self):
    return int( self.cget('signalperiod') )
     
  def calculate(self):
    pivot, s1, s2, s3 = Indicators.MACD( self.series['close'], 
                                fastperiod = self.fastperiod(),  
                                slowperiod = self.slowperiod(),
                                signalperiod = self.signalperiod() )
                                
    return ( pivot, common.padNans(s1, self.index), common.padNans(s2, self.index), common.padNans(s3, self.index) )
    
    
  def applyFlags(self, ts1, ts2):
    _sell_list = []
    _buy_list  = []
    direction  = None
    for i, direction in TS.roll_intersect(ts1, ts2):
      if direction:
        _buy_list.append( self.index[i] )
      else:
        _sell_list.append( self.index[i] )
                   
    return dict( sell = _sell_list, buy = _buy_list )
    
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts1, ts2, ts3 = self.calculate()
    
    flags = self.applyFlags(ts1, ts2)
    
    return ( [{ 
      'name'   : 'MACD-H%d' % self.signalperiod(),
      'series' : common.pd2json(ts3),
      'type'   : 'column'
    }, {
      'name'   : 'MACD',
      'series' : common.pd2json(ts1),
      'flags'  : flags
    }, {
      'name'   : 'MACD-Signal',
      'series' : common.pd2json(ts2)
    }], self.config() )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'fastperiod' : 12, 'slowperiod': 26, 'signalperiod': 9 })
    return dict( defaults.items() + kwgs.items() )
    
def impl(series, options):
  return MACD(series, options = options)