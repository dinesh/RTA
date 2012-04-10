import sys
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
  print_help_and_exit(sys.exc_info[1])
  
def ADX(*args):                       #requires (high, low, close, [timeperiod=14])
  return talib.ADX(*args)
  
def AVGPRICE(*args):                  #requires (open, high, low, close)
  return talib.AVGPRICE(*args)
  
def BBANDS(*args, **kwgs):
  return talib.BBANDS(*args, **kwgs)
  
def CCI(*args):                       #requires (high, low, close, [timeperiod=14])
  return talib.CCI(*args)

#Candlestick patterns
def CDL2CROWS(*args):                 #requires (open, high, low, close)     
  ''' NOT WORKING '''
  return talib.CDL2CROWS(*args)

#Candlestick patterns
def CDL3BLACKCROWS(*args):            #requires (open, high, low, close)
  ''' NOT WORKING '''
  return talib.CDL3BLACKCROWS(*args)

def DX(*args):                        #requires (high, low, close, [timeperiod=14])
  return talib.DX(*args)

def EMA(*args):                       #requires (
  return tablib.EMA(args)
  
def MIN(*args):
  return talib.MIN(*args)
  
def DEMA(*args, **kwgs):
  return talib.DEMA(*args, **kwgs)

def RSI(*args):                        #requires (real=(close)[, timeperiod=14])
  return talib.RSI(*args)

def SMA(*args):                        #requires (real=(close)[, timeperiod=30])
  return talib.SMA(*args)

def STDDEV(*args):                     #requires (real=(close)[, timeperiod=5, nbdev=1.000000e+0])
  return talib.STDDEV(*args)

def STOCH(*args):                     #requires (high, low, close[, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0])
  return talib.STOCH(*args)

def STOCHF(*args):                     #requires (high, low, close[, fastk_period=5, fastd_period=3, fastd_matype=0])
  return talib.STOCHF(*args)

def STOCHRSI(*args):                     #requires (real(=close)[, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0])
  return talib.STOCHRSI(*args)

def WILLR(*args):                     #requires (high, low, close, [timeperiod=14])
  return talib.WILLR(*args)
