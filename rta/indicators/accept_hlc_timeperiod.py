

from rta.api import Indicators
from rta import common
from rta import ts as TS

from . import IndicatorBase, IndicatorFactory
import numpy as np
import itertools

class AcceptOHLCTimeperiod(IndicatorBase):
  
  @property
  def timeperiod(self):
    return int(self.cget('timeperiod'))
    
  def calculate(self):
    pivot, s1 = getattr(Indicators, self.func).__call__( self.series['high'], 
                                                self.series['low'], 
                                                self.series['close'], 
                                                timeperiod = self.timeperiod )
                                
    return ( pivot, common.padNans(s1, self.index) )
    
        
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts1 = self.calculate()
    
    return ( [{ 
      'name'   : "%s(%d)" % ( self.func, self.timeperiod ),
      'series' : common.pd2json(ts1),
      'position' : 2
     }], self.config() )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'timeperiod' : 14 })
    return dict( defaults.items() + kwgs.items() )
    

[ IndicatorFactory.register(x, AcceptOHLCTimeperiod) for x in  [ 'ADX', 'ADXR', 'DX', 'MINUS_DI', 'PLUS_DI', 'WILLR' ] ]