

from rta.api import Indicators
from rta import common
from rta import ts as TS

from . import IndicatorBase
import numpy as np
import itertools

class BBANDS(IndicatorBase):
  
  # 1) should extract options, 2) call talib function 3) maketimeseries of output and return
  
  def timeperiod(self):
    return int( self.cget('timeperiod') )
  
  def nbdevup(self):
    return int( self.cget('nbdevup') )
  
  def nbdevdn(self):
    return int( self.cget('nbdevdn') )
  
  def matype(self):
    return int( self.cget('matype') )
     
  def calculate(self):
    pivot, s1, s2, s3 = Indicators.BBANDS( self.series['close'], 
                                self.timeperiod(),  
                                self.nbdevup(), self.nbdevdn(), self.matype() )
                                
    return ( pivot, common.padNans(s1, self.index), common.padNans(s2, self.index), common.padNans(s3, self.index) )
    
    
  def applyFlags(self, ts1, ts2):
    _overbought_list   = [ self.index[i] for (i, direction) in TS.roll_intersect(ts1, self.series['close']) if direction ] 
    _oversold_list = [ self.index[i] for (i, direction) in TS.roll_intersect(ts2, self.series['close'] ) if not direction ]
        
    return dict( oversold = _oversold_list, overbought = _overbought_list )
    
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts1, ts2, ts3 = self.calculate()
    
    flags = self.applyFlags(ts1, ts3)
    return ( [{ 
      'name'   : 'BBANDS-UP',
      'series' : common.pd2json(ts1),
      'flags'  : { 'overbought': common.pd2json( flags.get('overbought', []) ) } ,
      'position' : 0
    }, {
      'name'   : 'BBANDS-SMA',
      'series' : common.pd2json(ts2),
      'position' : 0
    }, {
      'name'   : 'BBANDS-DW',
      'series' : common.pd2json(ts3),
      'flags'  : { 'oversold': common.pd2json( flags.get('oversold', []) ) },
      'position' : 0
    }], self.__class__.options( self.options ) )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'timeperiod' : 20, 'nbdevdn': 2, 'nbdevup': 2, 'matype': 0, 'position': 'overlay' })
    return dict( defaults.items() + kwgs.items() )
    
def impl(series, options):
  return BBANDS(series, options = options)