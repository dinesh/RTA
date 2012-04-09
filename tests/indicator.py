
import helper
from datetime import datetime, timedelta
from rta.api import *

today = datetime.today()

series = Model.Quote.series('3MINDIA', today - timedelta(days=1000) )['close'].values

# test SMA
#print Indicators.SMA(series)


# test BBANDS
# print Indicators.BBANDS( series, timeperiod=20,
#                                  nbdevup=2.0, nbdevdn=2.0,
#                                  matype= TaLib.MA_EMA )

print Indicators.CDL2CROWS( series, series, series, series )                                 
print Indicators.CDL3BLACKCROWS( series, series, series, series )                                 
