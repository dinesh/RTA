
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
    

# most important indicator
def indicator_by_rating(rank = 5):
  s = Config['talib_indicators']
  return s[ s['Requirement'] == 5 ]['Function'].values


def getConfig(baseConfig = {}):
  default = {}
  root = default['root'] = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
  default['symbols'] = pandas.read_csv( os.path.join(root, 'data/companylist.csv') )['Symbol'].values
  
  indicator_csv = pandas.read_csv( os.path.join(root, 'data/TALIB_functions.csv') )
  default['talib_indicators'] = indicator_csv
  
  default['dbname'] = 'nse_eod'
  return default
  
Config = getConfig()