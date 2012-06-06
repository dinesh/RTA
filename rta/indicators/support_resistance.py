
import numpy as np
import pandas as pd

from . import IndicatorBase, IndicatorFactory
from rta import common

__all__ = [ 'impl', 'SupportResistance' ] 

class SupportResistance(IndicatorBase):
  def cutoff(self):
    return int( self.cget('cutoff') )
    
  def calculate(self):
    sr = self.series['close']
    idx = _support_resistance( sr, cutoff = self.cutoff() )
    return ( 0, common.padNans( sr[idx], index= self.index[idx] ) )
    
    
  def applyFlags(self, ts):
    pass
    
  # should return the ouput as json format for web api
  def as_json(self):
    _, ts = self.calculate()
    return ( [{ 
      'name'      : 'SupportResistance(%d)' % self.cutoff(),
      'series'    : common.pd2json(ts),
      'position'  : 0,
    }], self.config() )
  
  def cget(self, key ):
    return self.__class__.options( self.options ).get(key)
    
  @classmethod
  def options(_cls, kwgs):
    defaults = dict({ 'cutoff' : 5 })
    return dict( defaults.items() + kwgs.items() )
  
  
def _delta( X, end, start ):
    return 100 * abs( 1.0 * ( X[end] - X[start] ) / X[start] )
    


def _support_resistance( X, cutoff = 5 ):
    idx, indices = 0, [0]
    base = (0, X[0] )
    pivot = ( 0, X[0] )
    idx = 0
    pdelta = bdelta = None
    while idx < X.size:
        bdelta = _delta( X, idx, base[0] )
        pdelta = _delta( X, idx, pivot[0] )
        
        if pdelta >= cutoff:
           tolerance = ( idx - indices[-1] > 2) # the reversal takes sometime
           if ( abs( X[idx] - base[1] ) < abs( pivot[1] - base[1]) ) or ( abs(X[idx] - pivot[1]) > abs( base[1] - pivot[1]) ):
                indices.append( pivot[0])
                base = pivot
                pivot = ( idx, X[idx] )
                idx -= 1
                
        
        if bdelta >= cutoff:
            if abs( X[idx] - base[1] ) > abs( pivot[1] - base[1]):
                pivot = ( idx, X[idx] )
               
        idx += 1
    
    indices.append( pivot[0] )

    int_indices = [int(i) for i in indices]

    index, present, dummy = 0, False, 0
    strength = []
    dummy_list = []
    for item in int_indices:
        index, present, dummy = 0, False, 0
        if item != 0:
            upper_limit = int(item * 1.02)
            lower_limit = int(item * 0.98)
            for dummy_item in dummy_list:
                dummy = item
                index += 1
                if lower_limit <= dummy_item && upper_limit >= dummy_item:
                    dummy = dummy_item
                    present = True 
                    break
        if present:
            dummy_list.append(dummy_list.count(dummy) + 1)
        else: 
            dummy_list.append(0)
        dummy_list.append(dummy)
    
    return indices

IndicatorFactory.register('SUPPORTRESISTANCE', SupportResistance)
