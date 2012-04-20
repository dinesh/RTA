import sys, re
# you may need to modify arguements based on indicators
# TODO: add decorators for cached properties
# TODO: use __all__ for dynamic imports

# https://github.com/mrjbq7/ta-lib

import sys, inspect
import pandas, numpy

  
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
  LIST = dict()  
  for ind in ALL_INDICATORS:
    definition = inspect.getdoc( getattr(talib, ind) )
    params = re.findall("([\w]+)=\?", definition) 
    desc = re.findall( "\(.*\)\n\n(.*)$", definition)
    LIST[ind] = dict({ 'args': params, 'desc': desc[0], 'id': ind } )
    
    
except ImportError:
  raise
  # print_help_and_exit(sys.exc_info[1])

for ind in ALL_INDICATORS:
  globals()[ind] = getattr(talib, ind)

I_OUTPUT_THREE_SERIES = ['BBANDS']
I_ACCEPTS_ONE_VALUE_AND_TIMEPERIOD = [ 'SMA', 'EMA']
I_ACCEPTS_THREE_VALUE_AND_TIMEPERIOD = [ 'ADX', 'ADXR' ]
I_ACCEPTS_FOUR_VALUE = [ 'AVGPRICE' ]


def make_tseries(res, index ):
  # print res
  pivot = index.shape[0] - res.shape[0]
  print pivot
  
  print res
  
  return pandas.DataFrame( 
      index = index,
      data = numpy.concatenate( [ numpy.zeros(pivot, 'int'), res ] ), 
  ).to_records().tolist()
  
def calculate(series, ind_id, options):
  indicator = LIST[ind_id]
  
  period = int( options.get('timeperiod', 20) )
  
  o, h, l ,c, sindex = ( series['open'].values, 
                        series['high'].values, 
                        series['low'].values, 
                        series['close'].values, 
                        series.index )
                        
  if ind_id == 'BBANDS':
    nbdevup = float( options.get( 'nbdevup', 2.0) )
    nbdevdn = float( options.get( 'nbdevdn', 2.0) )
    matype = int( options.get('matype', 0) )
    
    pivot, s1, s2, s3 = getattr(talib, ind_id).__call__( c, period, nbdevup, nbdevdn, matype)  
    print pivot, s1.shape, s2.shape, s3.shape
    print sindex.shape
    
    return [{ 
        'name': 'BBAND_UPPER_%sx' % nbdevup , 
      ' series' :  make_tseries( s1, sindex[pivot:]) 
      }, { 
        'name': 'BBAND_SMA_%sd' % period, 
        'series' : make_tseries(s2, sindex[pivot:]) 
      }, { 
        'name' : 'BBAND_LOWER_%sx' % nbdevdn, 
        'series' : make_tseries( s3, sindex[pivot:])
      } ]
                         
  if ind_id in I_ACCEPTS_ONE_VALUE_AND_TIMEPERIOD:
    pivot, res = getattr(talib, ind_id).__call__( c, timeperiod = period)  
    return [{ 
        'name': '%s-%sd' % ( ind_id, period ) , 
        'series' :  make_tseries( res, sindex[pivot:]) 
      } ]
    
  elif ind_id in I_ACCEPTS_FOUR_VALUE:
    pivot, res = getattr(talib, ind_id).__call__( o, h,l, c )  
    return [{ 
        'name': '%s-%sd' % ( ind_id, period ) , 
        'series' :  make_tseries( res, sindex[pivot:]) 
      } ]
    
  elif ind_id in I_ACCEPTS_THREE_VALUE_AND_TIMEPERIOD:
    pivot, res = getattr(talib, ind_id).__call__( h, l , c, timeperiod = period)  
    return [{ 
        'name': '%s-%sd' % ( ind_id, period ) , 
        'series' :  make_tseries( res, sindex) 
      } ]
    
  else:
    raise NotImplementedError("%s is not implmented yet." % ind_id)
  

SUPPORTED_INDICATORS = [  'SMA', 'EMA', 'BBANDS', 'CDL2CROWS', 'MACD', 'MACDEXT'  ]

CANDLESTICK_INDICATORS = [ 'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3WHITESOLDIERS','CDLBREAKAWAY',
                           'CDLDARKCLOUDCOVER','CDLDOJI','CDLDOJISTAR','CDLDRAGONFLYDOJI',
                           'CDLENGULFING', 'CDLEVENINGDOJISTAR','CDLEVENINGSTAR','CDLGAPSIDESIDEWHITE',
                           'CDLGRAVESTONEDOJI','CDLHAMMER','CDLHANGINGMAN','CDLHARAMI','CDLHARAMICROSS',
                           'CDLINVERTEDHAMMER','CDLLONGLEGGEDDOJI','CDLMORNINGDOJISTAR','CDLMORNINGSTAR',
                           'CDLPIERCING','CDLSHOOTINGSTAR','CDLSPINNINGTOP','CDLUPSIDEGAP2CROWS']



NOT_INCLUDED = [ 'CDL3LINESTRIKE','CDL3OUTSIDE','CDL3STARSINSOUTH','CDLABANDONEDBABY', 'CDLADVANCEBLOCK', 
                 'CDLBELTHOLD','CDLCLOSINGMARUBOZU','CDLCONCEALBABYSWALL','CDLCOUNTERATTACK','CDLHIGHWAVE',
                 'CDLHIKKAKE','CDLHIKKAKEMOD','CDLHOMINGPIGEON','CDLIDENTICAL3CROWS','CDLINNECK',
                 'CDLKICKING','CDLKICKINGBYLENGTH','CDLLADDERBOTTOM','CDLLONGLINE','CDLMARUBOZU',
                 'CDLMATCHINGLOW','CDLMATHOLD','CDLONNECK','CDLRICKSHAWMAN','CDLRISEFALL3METHODS',
                 'CDLSEPARATINGLINES','CDLSHORTLINE','CDLSTALLEDPATTERN','CDLSTICKSANDWICH', 'CDLTAKURI',
                 'CDLTASUKIGAP','CDLTHRUSTING','CDLTRISTAR','CDLUNIQUE3RIVER','CDLXSIDEGAP3METHODS']
 