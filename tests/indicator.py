
import helper
from datetime import datetime, timedelta
from rta.api import *

today = datetime.today()

series = Model.Quote.series('3MINDIA', today - timedelta(days=100))['close']

# test SMA
print Indicators.SMA(series.values)


# test BBANDS
print Indicators.BBANDS( series.values, timeperiod=20,
                                 nbdevup=2.0, nbdevdn=2.0,
                                 matype= TaLib.MA_EMA )
                                 
