# https://github.com/mrjbq7/ta-lib

import sys, re, inspect

import pandas, numpy
  
  
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

I_ACCEPTS_ONE_VALUE = [ 'HT_TREANDLINE' ]  

I_ACCEPTS_TWO_VALUE_AND_TIMEPERIOD = ['MINUS_DM', 'PLUS_DM']

I_ACCEPTS_ONE_VALUE_AND_TIMEPERIOD = [ 'SMA', 'EMA', 'RSI', 'MAX', 'MIN', 'MIN', 'MOM' ]

I_ACCEPTS_THREE_VALUE_AND_TIMEPERIOD = [ 'ADX', 'ADXR', 'CCI', 'DX', 'MINUS_DI', 'PLUS_DI', 'WILLR' ]

I_ACCEPTS_FOUR_VALUE = [ 'AVGPRICE', 'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3WHITESOLDIERS', 'CDLDOJI', 'CDLDOJISTAR', 'CDLDRAGONFLYDOJI', 
                         'CDLGRAVESTONEDOJI', 'CDLENGULFING', 'CDLHAMMER', 'CDLHANGINGMAN', 'CDLHARAMI', 'CDLINVERTEDHAMMER', 'CDLPIERCING', 
                         'CDLSHOOTINGSTAR', 'CDLSPINNINGTOP', 'CDLHARAMICROSS'  ]

I_ACCEPTS_FOUR_VALUE_AND_PENETRATION = [ 'CDLDARKCLOUDCOVER', 'CDLEVENINGSTAR', 'CDLEVENINGDOJISTAR', 'CDLMORNINGDOJISTAR', 'CDLMORNINGSTAR' ]


def make_tseries(res, index ):
  return CoreApi.padNans(res, index).to_records().tolist()

class IndicatorBase(object):
  __slots__ = [ 'series', 'index' ]
  
  def __init__(self, series, **kwgs):
    self.series = series
    self.index = series.index
    self.options = kwgs.get('options', {})
    
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
                        
  if ind_id == 'BBANDS':
    nbdevup = float( options.get( 'nbdevup', 2.0) )
    nbdevdn = float( options.get( 'nbdevdn', 2.0) )
    matype = int( options.get('matype', 0) )
    
    pivot, s1, s2, s3 = getattr(talib, ind_id).__call__( c, period, nbdevup, nbdevdn, matype)  
    
    return [{ 
        'name': 'BBAND_UPPER_%sx' % nbdevup , 
        'series' :  make_tseries( s1, sindex) 
      }, { 
        'name': 'BBAND_SMA_%sd' % period, 
        'series' : make_tseries(s2, sindex) 
      }, { 
        'name' : 'BBAND_LOWER_%sx' % nbdevdn, 
        'series' : make_tseries( s3, sindex)
      } ]
  elif ind_id == 'HT_TRENDLINE':
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
    
  elif ind_id == 'MACD':
    fastperied = int( options.get('fastperied', 12) )
    slowperiod = int( options.get('slowperiod', 26 ) )
    signalperiod = int( options.get('signaltime', 9) )
    
    pivot, s1, s2, s3 = MACD(c, fastperied, slowperiod, signalperiod)
    return [{
      'name': 'MACD',
      'series': make_tseries( s1, sindex )
    }, {
      'name': 'signal_%sd' % signalperiod,
      'series': make_tseries( s2, sindex )
    }, {
      'name': 'MACD_HIST',
      'series': make_tseries(s3, sindex )
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
    
  elif ind_id in I_ACCEPTS_FOUR_VALUE:
    pivot, res = getattr(talib, ind_id).__call__( o, h,l, c )  
    return [{ 
        'name': '%s-%sd' % ( ind_id, period ) , 
        'series' :  make_tseries( res, sindex) 
      } ]
  
  
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
 