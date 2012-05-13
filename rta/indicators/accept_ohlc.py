

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
                                
    return ( pivot, common.padNans(s1, self.index) )
    
    
  def applyFlags(self, ts1, ts2):
    _overbought_list   = [ self.index[i] for (i, direction) in TS.roll_intersect(ts1, self.series['close']) if direction ] 
    _oversold_list = [ self.index[i] for (i, direction) in TS.roll_intersect(ts2, self.series['close'] ) if not direction ]
        
    return dict( oversold = _oversold_list, overbought = _overbought_list )
    
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
    return dict()

[ IndicatorFactory.register(x, AcceptOHLC) for x in [ 'AVGPRICE', 'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3WHITESOLDIERS', 'CDLDOJI', 
  'CDLDOJISTAR', 'CDLDRAGONFLYDOJI', 'CDLGRAVESTONEDOJI', 'CDLENGULFING', 
  'CDLHAMMER', 'CDLHANGINGMAN', 'CDLHARAMI', 'CDLINVERTEDHAMMER', 
  'CDLPIERCING', 'CDLSHOOTINGSTAR', 'CDLSPINNINGTOP', 'CDLHARAMICROSS'  ] ]