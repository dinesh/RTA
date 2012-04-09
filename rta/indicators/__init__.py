
# you may need to modify arguements based on indicators
# TODO: add decorators for cached properties
# TODO: use __all__ for dynamic imports

# https://github.com/mrjbq7/ta-lib

SUPPORTED_INDICATORS = [ 'MIN', 'SMA', 'EMA' ]

  
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
except ImportError:
  print_help_and_exit(sys.exec_info[1])
  
def MIN(*args):
  return talib.MIN(*args)
  
def SMA(*args):
  return talib.SMA(*args)

def EMA(*args):
  return tablib.EMA(args)
  
def BBANDS(*args, **kwgs):
  return talib.BBANDS(*args, **kwgs)
  
def DEMA(*args, **kwgs):
  return talib.DEMA(*args, **kwgs)
  
  
def CDL2CROWS(*args, **kwgs):
  return talib.CDL2CROWS(*args, **kwgs)

def CDL3BLACKCROWS(*args, **kwgs):
  return talib.CDL3BLACKCROWS(*args, **kwgs)
  