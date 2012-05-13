# https://github.com/mrjbq7/ta-lib

import sys, re, inspect, glob, os, imp
import pandas, numpy
from rta import common

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
  
  LIST['ZIGZAG'] = dict( args=['cutoff'], desc= 'ZigZag indicatpr', id='ZIGZAG' )
  
except ImportError:
  raise

for ind in ALL_INDICATORS:
  globals()[ind] = getattr(talib, ind)

__all__ = ['LIST', 'IndicatorFactory', 'IndicatorList' ]

I_ACCEPTS_ONE_VALUE = [ 'HT_TREANDLINE' ]  
I_ACCEPTS_TWO_VALUE_AND_TIMEPERIOD = ['MINUS_DM', 'PLUS_DM']
I_ACCEPTS_ONE_VALUE_AND_TIMEPERIOD = [ 'SMA', 'EMA', 'RSI', 'MAX', 'MIN', 'MIN', 'MOM' ]
I_ACCEPTS_FOUR_VALUE_AND_PENETRATION = [ 'CDLDARKCLOUDCOVER', 'CDLEVENINGSTAR', 'CDLEVENINGDOJISTAR', 'CDLMORNINGDOJISTAR', 'CDLMORNINGSTAR' ]


def make_tseries(res, index ):
  return CoreApi.padNans(res, index).to_records().tolist()

def register_indicators():
  try:
    for pyfile in glob.glob( os.path.join( os.path.dirname(__file__), '*.py') ):
      if not os.path.basename(pyfile) == '__init__.py':
        __import__(pyfile)
  except Exception:
    raise
      
class IndicatorFactory(object):
  __slots__ = []
  __registery__ = {}
  
  @classmethod
  def register(_cls, key, impl):
    val = _cls.__registery__.get( key, None)
    if val:
      print "{func} is already registered from {module}!!! omg".format( func = key, module = val )
    else:
      print "\t >> {func} registerd from {module}: success".format( func = key, module = inspect.getfile(impl)  )
      _cls.__registery__[ key ] = impl
    
  @classmethod
  def run(_cls, func, series, options):
    cls = _cls.__registery__.get(func, None)
    if cls:
     return cls( series, options= options, func=func )
    else:
      raise NotImplementedError(func)
  
class IndicatorBase(object):
  __slots__ = [ 'series', 'index', 'func', 'options' ]
  
  def __init__(self, series, **kwgs):
    self.series = series
    self.index = series.index
    self.options = kwgs.get('options', {})
    self.func = kwgs.get('func', None)

  def as_json(self):
    raise NotImplementedError("%s should implement as_json function")
    
  def calculate(self):
    raise NotImplementedError("%s should implement calculate function")
    
  def config(self):
    return self.__class__.options( self.options )  
    
      
    
def calculate(series, ind_id, options):
  indicator = LIST[ind_id]
  
  period = int( options.get('timeperiod', 20) )
  
  o, h, l ,c, sindex = ( series['open'].values, 
                        series['high'].values, 
                        series['low'].values, 
                        series['close'].values, 
                        series.index )
                        
  if ind_id == 'HT_TRENDLINE':
    pivot, res = HT_TRENDLINE(c)
    return [{
      'name': 'HT_TRENDLINE',
      'series': make_tseries( res, sindex )
    }]
  
  elif ind_id == 'STDDEV':
    nbdev = int( options.get('nbdev', 1 ) )
    pivot, res = STDDEV(c, period, nbdev )
    return [{
      'name': 'STDDEV-%sd' % period ,
      'series': make_tseries( res, sindex )
    }]  
  elif ind_id == 'STOCH':
    fastk_period = int( options.get('fastk_period', 5))
    slowk_period = int( options.get('slowk_period', 3))
    slowk_matype = int( options.get('slowk_matype', 0 ) )
    slowd_period = int( options.get('slowd_period',  3) )
    slowd_matype = int( options.get('slowd_matype', 0) )   
    
    pivot, s1, s2 = STOCH(h,l,c, fastk_period, slowk_period, slowk_matype, slowd_period, slowd_matype )
    return [{
      'name': 'STOCH_SLOWK',
      'series': make_tseries( s1, sindex )
    }, {
      'name': 'STOCH_SLOWD',
      'series': make_tseries( s2, sindex )
    }]
    
  elif ind_id == 'STOCHF':
    fastk_period = int( options.get('fastk_period', 5))
    fastd_period = int( options.get('fastd_period', 3 ))
    fastd_matype = int( options.get('fastd_matype', 0) )
    
    pivot, s1, s2 = STOCH(h,l,c, fastk_period, fastd_period, fastd_matype )
    return [{
      'name': 'STOCHF_FASTK',
      'series': make_tseries( s1, sindex )
    }, {
      'name': 'STOCHF_FASTD',
      'series': make_tseries( s2, sindex )
    }]
    
  elif ind_id == 'STOCHRSI':
    fastk_period = int( options.get('fastk_period', 5))
    fastd_period = int( options.get('fastd_period', 3 ))
    fastd_matype = int( options.get('fastd_matype', 0) )
    
    pivot, s1, s2 = STOCH(h,l,c, period, fastk_period, fastd_period, fastd_matype )
    return [{
      'name': 'STOCHRSI_FASTK',
      'series': make_tseries( s1, sindex )
    }, {
      'name': 'STOCHRSI_FASTD',
      'series': make_tseries( s2, sindex )
    }]
    
  
  elif ind_id in I_ACCEPTS_ONE_VALUE:
    pivot, res = getattr(talib, ind_id).__call__( c )  
    return [{ 
        'name': '%s' % ind_id , 
        'series' :  make_tseries( res, sindex) 
      } ]

  elif ind_id in I_ACCEPTS_ONE_VALUE_AND_TIMEPERIOD:
    pivot, res = getattr(talib, ind_id).__call__( c, timeperiod = period)  
    return [{ 
        'name': '%s-%sd' % ( ind_id, period ) , 
        'series' :  make_tseries( res, sindex) 
      }]
    
  
  elif ind_id in I_ACCEPTS_TWO_VALUE_AND_TIMEPERIOD:
    pivot, res = getattr(talib, ind_id).__call__( h, l, period )  
    return [{ 
        'name': '%s-%sd' % ( ind_id, period ) , 
        'series' :  make_tseries( res, sindex) 
      } ]
        
  elif ind_id in I_ACCEPTS_THREE_VALUE_AND_TIMEPERIOD:
    pivot, res = getattr(talib, ind_id).__call__( h, l , c, timeperiod = period)  
    return [{ 
        'name': '%s-%sd' % ( ind_id, period ) , 
        'series' :  make_tseries( res, sindex) 
      } ]
  elif ind_id in I_ACCEPTS_FOUR_VALUE_AND_PENETRATION:
    penetration = int( options.get('penetration', 20) )
    pivot, res = getattr(talib, ind_id).__call__( o, h, l , c, penetration= penetration)  
    return [{ 
        'name': '%s' % ( ind_id ) , 
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
 