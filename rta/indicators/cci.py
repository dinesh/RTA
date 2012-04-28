
from rta.api import Indicators
from rta import common

from . import IndicatorBase
import numpy as np


class CCI(IndicatorBase):
  
  # 1) should extract options, 2) call talib function 3) maketimeseries of output and return
  
  def timeperiod(self):
    return int( self.cget('timeperiod') )
    
  def calculate(self):
    pivot, s = Indicators.CCI( self.series['high'], self.series['low'], 
                               self.series['close'], timeperiod = self.timeperiod() )
    return ( pivot, common.padNans(s, self.index) )
    
    
  def applyFlags(self, ts):
    _sell_list = []
    _buy_list  = []
    direction  = None
    
    for _prev, _current, _next in common.batch( ts.iteritems(), 3):
      
      _, prev      = _prev
      idx, current = _current
      _, next      = _next
      
      slope = next + prev - 2 * current
      direction = 'asc' if slope > 0 else 'desc'
      
      # buy
      if prev <= -100 and next > -100 :
        if direction == 'asc':
          _buy_list.append( idx)
          
      # sell
      if prev >= 100 and next < 100 :
        if direction == 'desc':
          _sell_list.append(idx)
        
    return dict( sell = _sell_list, buy = _buy_list )
    
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts = self.calculate()
    flags = self.applyFlags(ts)
    return [{ 
      'name'   : 'CCI-%d' % self.timeperiod(),
      'series' : common.pd2json(ts),
      'flags'  : flags,
    }]
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'timeperiod' : 14 })
    return dict( defaults.items() + kwgs.items() )
    
def impl(series, options):
  return CCI(series, options = options)