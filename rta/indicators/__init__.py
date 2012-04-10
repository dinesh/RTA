import sys
# you may need to modify arguements based on indicators
# TODO: add decorators for cached properties
# TODO: use __all__ for dynamic imports

# https://github.com/mrjbq7/ta-lib
import sys, inspect

SUPPORTED_INDICATORS = [  'SMA', 'EMA', 'BBANDS', 'CDL2CROWS', 'MACD', 'MACDEXT',  ]



CANDLESTICK_INDICATORS = [ 'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3WHITESOLDIERS','CDLBREAKAWAY','CDLDARKCLOUDCOVER','CDLDOJI','CDLDOJISTAR','CDLDRAGONFLYDOJI','CDLENGULFING', 'CDLEVENINGDOJISTAR','CDLEVENINGSTAR','CDLGAPSIDESIDEWHITE','CDLGRAVESTONEDOJI','CDLHAMMER','CDLHANGINGMAN','CDLHARAMI','CDLHARAMICROSS','CDLINVERTEDHAMMER','CDLLONGLEGGEDDOJI','CDLMORNINGDOJISTAR','CDLMORNINGSTAR','CDLPIERCING','CDLSHOOTINGSTAR','CDLSPINNINGTOP','CDLUPSIDEGAP2CROWS']



NOT_INCLUDED = ['CDL3LINESTRIKE','CDL3OUTSIDE','CDL3STARSINSOUTH','CDLABANDONEDBABY', 'CDLADVANCEBLOCK','CDLBELTHOLD','CDLCLOSINGMARUBOZU','CDLCONCEALBABYSWALL','CDLCOUNTERATTACK','CDLHIGHWAVE','CDLHIKKAKE','CDLHIKKAKEMOD','CDLHOMINGPIGEON','CDLIDENTICAL3CROWS','CDLINNECK','CDLKICKING','CDLKICKINGBYLENGTH','CDLLADDERBOTTOM','CDLLONGLINE','CDLMARUBOZU','CDLMATCHINGLOW','CDLMATHOLD','CDLONNECK','CDLRICKSHAWMAN','CDLRISEFALL3METHODS','CDLSEPARATINGLINES','CDLSHORTLINE','CDLSTALLEDPATTERN','CDLSTICKSANDWICH', 'CDLTAKURI','CDLTASUKIGAP','CDLTHRUSTING','CDLTRISTAR','CDLUNIQUE3RIVER','CDLXSIDEGAP3METHODS']
  
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

for ind in ALL_INDICATORS:
  globals()[ind] = getattr(talib, ind)
