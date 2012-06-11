

from rta.api import Indicators
from rta import common
from rta import ts as TS

from . import IndicatorBase, IndicatorFactory
import numpy as np
import itertools

class AcceptOHLC(IndicatorBase):
  
  def calculate(self):
    pivot, s1 = getattr(Indicators, self.func).__call__( self.series['open'], 
                                                         self.series['low'],  
                                                         self.series['high'], 
                                                         self.series['close'] )
    
    print s1                           
    return ( pivot, common.padNans(s1, self.index) )
    
    
  def applyFlags(self, ts):
    return ts[ts > 0]
    
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts1 = self.calculate()
    flags =  common.pd2json( self.applyFlags(ts1) )
    
    return ( [{ 
      'name'   : self.func,
      'series' : flags,
      'position' : 0
     }], self.config() )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    return dict()

[ IndicatorFactory.register(x, AcceptOHLC) for x in [ 'AVGPRICE', 'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3WHITESOLDIERS', 'CDLDOJI', 
  'CDLDOJISTAR', 'CDLDRAGONFLYDOJI', 'CDLGRAVESTONEDOJI', 'CDLENGULFING', 
  'CDLHAMMER', 'CDLHANGINGMAN', 'CDLHARAMI', 'CDLINVERTEDHAMMER', 
  'CDLPIERCING', 'CDLSHOOTINGSTAR', 'CDLSPINNINGTOP', 'CDLHARAMICROSS'  ] ]