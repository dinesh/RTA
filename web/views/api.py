from flask import *
from flask.views import MethodView, View
from functools import wraps
import datetime, time, operator, calendar, random
import numpy as np
import os

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs) ) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function

current_dir = os.path.dirname( os.path.abspath(__name__))
from rta import api as CoreApi


class Api:
  def __init__(self, app, prefix = '/api'):
    self.app = app
    self.prefix = prefix
    self.setup()
    
  def setup(self):
    pass
    
  def configure_routes(self):
    
    routes = [ 
          ( (self.app, self.prefix),
                  ('/indicators/<indicator>/<symbol>/series.json', self.get_indicator_series ),
                  ('/indicators', self.get_indicators ),
                  ('/quotes/<symbol>.json', self.get_quotes),
                  ('/symbols.json', self.get_symbols),
          ),
    ]
    
    
    for route in routes:
        # endpoint: (blueprint_instance, url_prefix)
        # rules: [('/route/', view_function), ...]
        
        endpoint, rules = route[0], route[1:]
        
        for pattern, view in rules:
          if self.prefix:
            pattern = self.prefix + pattern
        
          if endpoint is None:
              self.app.add_url_rule( pattern, view_func=view)
          else:
            endpoint[0].add_url_rule(pattern, view_func=view)
       
  @support_jsonp  
  def get_indicators(self):
    __list, data = CoreApi.Indicators.LIST, list()
    for func in CoreApi.Configuration.indicator_by_rating(5):
      data.append( __list[func.strip()] )
      
    return json.dumps({ 'indicators': data })
  
  @support_jsonp
  def get_indicator_series(self, indicator, symbol):
    start  = request.args.get('start')
    end    = request.args.get('end')
    args   = request.args.get('params', {})
    
    # dividing by zero here b/c javascript returns time in ms
    if start:
      start = datetime.datetime.fromtimestamp( int(start) / 1000)
    if end:
      end = datetime.datetime.fromtimestamp( int(end) / 1000 )
    
    price  = CoreApi.Model.Quote.series(symbol, start = start, end = end )
    
    if price.shape[0] > 0:
      # res, _config = getattr( CoreApi, indicator.lower() ).impl( price, request.args ).as_json()
      res, _config = CoreApi.IndicatorFactory.run( indicator, price, request.args ).as_json()
      return json.dumps({ 'records': res, 'settings': _config }, cls = CoreApi.JSONEncoder )
    else:
      return json.dumps({ 'records' : []})
    
  @support_jsonp
  def get_quotes(self, symbol):
    symbol   = symbol or request.args.get('symbol', False)
    fields   = request.args.get('fields', ['tick', 'open', 'high', 'low', 'close' ] )
    page     = request.args.get('page', 1)
    per_page = request.args.get('per_page', 3 * 360)
    
    if symbol:
      cursor = CoreApi.Model.Quote.scope().find( { 
                  'symbol': symbol 
                }, fields = fields + [ 'volume' ] 
                ).limit(per_page).skip( (page -1) * per_page ).sort('tick')
                
      records = [ [ x[key] for key in fields ] for x in cursor ]
      volume =  [ [ x['tick'] , x['volume'] ] for x in cursor.rewind() ]      
      
      return json.dumps(dict( { 
        'records' : records,
        'volume'  : volume
      }), cls = CoreApi.JSONEncoder)
      
    else:
      return "Bad Request: %s not found" % symbol, 404 
  
  @support_jsonp
  def get_symbols(self):
    return json.dumps({ 'records': [ x for x in CoreApi.Config['symbols'] ]  } )