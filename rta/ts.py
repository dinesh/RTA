

import numpy as np

__all__ = ['roll_intersect', 'roll_trendline']

def roll_intersect(x,y):
  X, Y = np.asarray(x), np.asarray(y)
  diff = X > Y
  shifted_diff = np.insert( diff[:-1], 0, [False] )
  indices = np.nonzero( np.logical_xor( diff, shifted_diff ) )[0]
  print indices

  return [ (i, x[i] > x[i-1] ) for i in indices if i < x.shape[0] -1 ]

def roll_trendline(x, y, *args):
  _x = np.arange( len(x) )
  p = np.poly1d( np.polyfit(_x, y, 1) )
  return [ [x[i], v] for i,v in enumerate(p(_x)) ]
  