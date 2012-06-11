

from rta.api import Indicators
from rta import common
from rta import ts as TS

from . import IndicatorBase, IndicatorFactory
import numpy as np
import itertools

class AcceptCTimeperiod(IndicatorBase):
  
  @property
  def timeperiod(self):
    return int( self.cget('timeperiod') )
  
  def calculate(self):
    pivot, s1 = getattr(Indicators, self.func).__call__(  self.series['close'], timeperiod = self.timeperiod )
                                
    return ( pivot, common.padNans(s1, self.index) )
    
    
  def applyFlags(self, ts1, ts2):
    pass
    
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts1 = self.calculate()
    
    return ( [{ 
      'name'   : self.func,
      'series' : common.pd2json(ts1),
      'position' : 0,
     }], self.config() )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'timeperiod' : 14 })
    return dict( defaults.items() + kwgs.items() )

[ IndicatorFactory.register(x, AcceptCTimeperiod) for x in [ 'SMA', 'EMA', 'MAX', 'MIN', 'MOM' ] ]