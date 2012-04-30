
from rta.api import Indicators
from rta import common
from rta import ts as TS

from . import IndicatorBase
import numpy as np


class RSI(IndicatorBase):
  
  def timeperiod(self):
    return int( self.cget('timeperiod') )
    
  def calculate(self):
    pivot, s = Indicators.RSI( self.series['close'], timeperiod = self.timeperiod() )
    return ( pivot, common.padNans(s, self.index) )
    
    
  def applyFlags(self, ts):
    _sell_list = []
    _buy_list  = []
    direction  = None
    
    _sell_list = [ ts.index[i] for (i, slope) in TS.roll_intersect(ts, 70) if slope ]
    _buy_list = [ ts.index[i] for (i, slope) in TS.roll_intersect(ts, 30) if not slope ]
    
    return dict( sell = _sell_list, buy = _buy_list )
    
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts = self.calculate()
    flags = self.applyFlags(ts)
    return [{ 
      'name'   : 'RSI-%d' % self.timeperiod(),
      'series' : common.pd2json(ts),
      'flags'  : flags,
      'position' : 2
    }]
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'timeperiod' : 14 })
    return dict( defaults.items() + kwgs.items() )
    
def impl(series, options):
  return RSI(series, options = options)