
import os, sys
import pandas

# not using now
def cached(func):
  cache = {}
  def new_func(*args):
      if args in cache:
           return cache[args]
      else:
           temp = cache[args] = func(*args)
           return temp
  return new_func
    

def getConfig(baseConfig = {}):
  default = {}
  root = default['root'] = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
  default['symbols'] = pandas.read_csv( os.path.join(root, 'data/companylist.csv') )['Symbol'].values
  default['dbpath'] = os.path.join( root, 'data', 'rta_dev.hd5' )
  return default
  
config = getConfig()