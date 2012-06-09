
import numpy as np
import pandas as pd

from . import IndicatorBase, IndicatorFactory
from rta import common

__all__ = [ 'impl', 'SupportResistance' ] 

class SupportResistance(IndicatorBase):
  
  @property
  def cutoff(self):
    return int( self.cget('cutoff') )
  
  @property
  def numlines(self):
    return int(self.cget('numlines'))
      
  def calculate(self):
    _series         = self.series['open']
    tkidx           = common._sr( _series, cutoff = self.cutoff, delta = 10, lines = self.numlines )
    return tkidx
    
  def applyFlags(self, ts):
    pass
    
  # should return the ouput as json format for web api
  def as_json(self):
    ts = self.calculate()
    return ( [{
      'series'    : [],
      'flags'     : { 'sr' : common.pd2json(ts) },
      'position'  : 0,
    }], self.config() )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'cutoff' : 5, 'numlines': 5 })
    return dict( defaults.items() + kwgs.items() )
  
  
def _delta( X, end, start ):
    return 100 * abs( 1.0 * ( X[end] - X[start] ) / X[start] )
    

IndicatorFactory.register('S-R', SupportResistance)
