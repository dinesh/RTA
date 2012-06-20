from datetime import date, datetime
import calendar
import numpy
import pandas

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


class ObjectEncoder(json.JSONEncoder):
    '''
    Encode any object with the method as_json on it.
    '''
    def default(self, obj):
        if hasattr(obj, 'as_json'):
            return obj.as_json()
        elif isinstance( obj, pandas.Series):
            return obj.iteritems()
        elif isinstance( obj, pandas.DataFrame):
            return obj.iterrows()
        elif isinstance(obj, (numpy.ndarray, numpy.float64, numpy.int64) ):
            if len(obj.shape) == 0:
                return float(obj)
            else:
                return [float(x) for x in obj]                        
        elif isinstance(obj, (datetime, date)):
            return calendar.timegm(obj.timetuple()) * 1000
        else:
            return super(ObjectEncoder, self).default(obj)


def dump_json(chart):
    '''Dumps a chart to json'''
    return json.dumps(chart, cls=ObjectEncoder)
