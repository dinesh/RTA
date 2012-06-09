
import numpy as np
import pandas as pd

from . import IndicatorBase, IndicatorFactory
from rta import common

__all__ = [ 'impl', 'Zigzag' ] 

class Zigzag(IndicatorBase):
  def cutoff(self):
    return int( self.cget('cutoff') )
    
  def calculate(self):
    sr = self.series['open']
    idx = common._zigzag( sr, cutoff = self.cutoff() )
    return ( 0, common.padNans( sr[idx], index= self.index[idx] ) )
    
    
  def applyFlags(self, ts):
    pass
    
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts = self.calculate()
    return ( [{ 
      'name'      : 'ZigZag(%d)' % self.cutoff(),
      'series'    : common.pd2json(ts),
      'position'  : 0,
    }], self.config() )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'cutoff' : 5 })
    return dict( defaults.items() + kwgs.items() )
  


IndicatorFactory.register('ZIGZAG', Zigzag)