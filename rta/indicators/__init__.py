

# Lazzy import for _tablib
# you may need to modify arguements based on indicators
# add decorators for cached properties

# may refer to https://github.com/mlamby/indicator

SUPPORTED_INDICATORS = [ 'SMA', 'EMA' ]

def _talib():
  import TaLib
  
def SMA(*args):
  _talib().TA_SMA(args)

def EMA(*args):
  _tablib().TA_EMA(args)
  