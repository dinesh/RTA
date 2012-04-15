from flask import *
from flask.views import MethodView, View
from functools import wraps
import datetime, time, operator, calendar
from pymongo.objectid import ObjectId

json = None
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            # Google Appengine offers simplejson via django
            from django.utils import simplejson as json
        except ImportError:
            json_available = False

class JSONEncoder(json.JSONEncoder):
    """Default implementation of :class:`json.JSONEncoder` which provides
    serialization for :class:`datetime.datetime` objects (to ISO 8601 format).

    .. versionadded:: 0.9

    """

    def default(self, obj):
        """Provides serialization for :class:`datetime.datetime` objects (in
        addition to the serialization provided by the default
        :class:`json.JSONEncoder` implementation).

        If `obj` is a :class:`datetime.datetime` object, this converts it into
        the corresponding ISO 8601 string representation.

        """
        if isinstance(obj, datetime.datetime):
            # this is for javascript series date utctime * 1000
            return calendar.timegm( obj.utctimetuple() ) * 1000
        if isinstance(obj, ObjectId):
          return str(obj)
          
        return super(JSONEncoder, self).default(obj)

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

import os
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
                  ('/indicators', self.get_indicators ),
                  ('/indicators/std', self.get_indicators),
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
    data = [ v for k, v in CoreApi.Indicators.LIST.items() ]
    return json.dumps({ 'indicators': data[:10] })
  
  @support_jsonp
  def get_quotes(self, symbol):
    symbol   = symbol or request.args.get('symbol', False)
    fields   = request.args.get('fields', ['tick', 'open', 'high', 'low', 'close' ] )
    page     = request.args.get('page', 1)
    per_page = request.args.get('per_page', 100)
    
    if symbol:
      cursor = CoreApi.Model.Quote.scope().find( { 'symbol': symbol },  fields = fields)\
                            .sort('tick')\
                            .limit(per_page)\
                            .skip( (page -1) * per_page ) 
      return json.dumps(dict( { 
        'records' : [ [ x[key] for key in fields ] for x in cursor ],
        'volume'  : [ [ x['tick'] , x['volume'] ] for x in cursor ]
      }), cls = JSONEncoder)
      
    else:
      return "Bad Request: %s not found" % symbol, 404 
  
  @support_jsonp
  def get_symbols(self):
    return json.dumps({ 'records': [ x for x in CoreApi.Config['symbols'] ]  } )