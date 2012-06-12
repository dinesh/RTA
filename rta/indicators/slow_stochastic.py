

from rta.api import Indicators
from rta import common
from rta import ts as TS

from . import IndicatorBase, IndicatorFactory
import numpy as np
import itertools

class SlowStochastic(IndicatorBase):
  
  @property
  def fastk_period(self):
    return int( self.cget('fastk_period') )
  
  @property
  def slowk_period(self):
    return int( self.cget('slowk_period') )
  
  @property
  def slowk_matype(self):
    return int( self.cget('slowk_matype') )
  
  @property
  def slowd_period(self):
    return int( self.cget('slowd_period') )
  
  @property
  def slowd_matype(self):
    return int( self.cget('slowd_matype') )
  
  def calculate(self):
    pivot, s1, s2 = getattr(Indicators, self.func).__call__( self.series['high'], self.series['low'], self.series['close'], self.fastk_period, self.slowk_period, self.slowk_matype, self.slowd_period, self.slowd_matype )
                                
    return ( pivot, common.padNans(s1, self.index), common.padNans(s2, self.index) )
    
    
  def applyFlags(self, ts1, ts2):
    pass
    
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts1, ts2 = self.calculate()
    
    return ( [{ 
      'name'   : 'STOCH-K',
      'series' : common.pd2json(ts2),
      'position' : 2,
     },{ 
      'name'   : 'STOCH-D',
      'series' : common.pd2json(ts1),
      'position' : 2,
     }], self.config() )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'fastk_period' : 5, 'slowk_period' : 3, 'slowk_matype' : 0, 'slowd_period' : 3, 'slowd_matype' : 0 })
    return dict( defaults.items() + kwgs.items() )

[ IndicatorFactory.register(x, SlowStochastic) for x in [ 'STOCH' ] ]
