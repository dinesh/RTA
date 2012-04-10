import sys
# you may need to modify arguements based on indicators
# TODO: add decorators for cached properties
# TODO: use __all__ for dynamic imports

# https://github.com/mrjbq7/ta-lib
import sys, inspect

SUPPORTED_INDICATORS = [  'SMA', 'EMA', 'BBANDS', 'CDL2CROWS', 'MACD', 'MACDEXT',  ]
  
def print_help_and_exit(msg):
  help = """
    Unable to load talib module.
    Please go to rta/src/talib and follow steps.
    1. make generate
    2. python setup.py build_ext --inplace
    3. to test
      $] nosetests
      
  """
  print help
  
  print "Program Exit bc/ " + msg
  
  
try:
  from rta.src.talib import talib 
  from rta.src.talib import functs
  ALL_INDICATORS = functs.descriptions
  for ind in ALL_INDICATORS:
    doc = inspect.getdoc( getattr(talib, ind) )
    
except ImportError:
  raise
  # print_help_and_exit(sys.exc_info[1])

for ind in SUPPORTED_INDICATORS:
  globals()[ind] = getattr(talib, ind)
