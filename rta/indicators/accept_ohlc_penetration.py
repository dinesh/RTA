

from rta.api import Indicators
from rta import common
from rta import ts as TS

from . import IndicatorBase, IndicatorFactory
import numpy as np
import itertools

class AcceptOHLCPeneteration(IndicatorBase):
  
  def calculate(self):
    pivot, s1 = getattr(Indicators, self.func).__call__( self.series['open'], self.series['high'], 
                                                self.series['low'], 
                                                self.series['close'], 
                                                penetration = int(self.cget('penetration')) )
    
    return ( pivot, common.padNans(s1, self.index) )
    
        
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts1 = self.calculate()
    
    return ( [{ 
      'name'   : self.func,
      'series' : common.pd2json(ts1),
      'position' : 0
     }], self.config() )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'penetration' : 20 })
    return dict( defaults.items() + kwgs.items() )
    

# [ IndicatorFactory.register(x, AcceptOHLCPeneteration ) for x in  [ 'CDLDARKCLOUDCOVER', 'CDLEVENINGSTAR', 'CDLEVENINGDOJISTAR', 'CDLMORNINGDOJISTAR', 'CDLMORNINGSTAR' ] ]