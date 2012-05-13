
import numpy as np

def _delta( X, end, start ):
    return 100 * abs( 1.0 * ( X[end] - X[start] ) / X[start] )
    

def _zigzag( X, cutoff = 5 ):
    idx, indices = 0, [0]
    base = (0, X[0] )
    pivot = ( 0, X[0] )
    idx = 0
    pdelta = bdelta = None
    while idx < X.size:
        bdelta = _delta( X, idx, base[0] )
        pdelta = _delta( X, idx, pivot[0] )
        
        if pdelta > cutoff:
           if abs( X[idx] - base[1] ) < abs( pivot[1] - base[1]):
                indices.append( pivot[0])
                base = pivot
                pivot = ( idx, X[idx] )
                idx -= 1
        
        if bdelta > cutoff:
            if abs( X[idx] - base[1] ) > abs( pivot[1] - base[1]):
                pivot = ( idx, X[idx] )
               
        idx += 1
    
    indices.append( pivot[0] )
        
    return indices