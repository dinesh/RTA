
from itertools import islice, chain, tee
import datetime
import calendar
from pymongo.objectid import ObjectId
import pandas
import numpy

def batch(iterable, size):
    sourceiter = iter(iterable)
    while True:
      batchiter = islice(sourceiter, size)  
      sizeiter, batchiter = tee( batchiter, 2)
      isize = len(list(sizeiter))
      if isize < size:
        raise StopIteration
      yield chain([ batchiter.next()], batchiter)



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

def padNans(res, index ):
  # print res
  pivot = index.shape[0] - res.shape[0]
  return pandas.Series( 
      index = index,
      data = numpy.concatenate( [ numpy.zeros(pivot, 'int'), res ] ), 
  )

def pd2json(df):
  if isinstance(df, pandas.DataFrame):
    return df.to_records().tolist()
  elif isinstance( df, pandas.Series ) or isinstance( df, pandas.TimeSeries ):
    return list( df.iteritems() )
  elif isinstance(df, pandas.Index ):
    return df.tolist()
  
__all__ = [ 'batch', 'JSONEncoder', 'padNans', 'pd2json' ]
