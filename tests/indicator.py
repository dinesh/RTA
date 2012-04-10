
import helper
from datetime import datetime, timedelta
from rta.api import *

today = datetime.today()

close = Model.Quote.series('3MINDIA', today - timedelta(days=100))['close']

# test SMA
print Indicators.SMA(close.values, 9)

# test SMA
#print Indicators.SMA(series)

# test ADX
print Indicators.ADX(close.values, close.values, close.values)

# test AVGPRICE
print Indicators.AVGPRICE(close.values, close.values, close.values, close.values)

# test BBANDS
print Indicators.BBANDS( close.values, timeperiod=20,
                                 nbdevup=2.0, nbdevdn=2.0,
                                 matype= TaLib.MA_EMA )
                                 
# test CANDLESTICK TWO CROWS
'''NOT WORKING'''
print Indicators.CDL2CROWS(close.values, close.values, close.values, close.values)

# test CANDLESTICK THREE BLACK CROWS
'''NOT WORKING'''
print Indicators.CDL3BLACKCROWS(close.values, close.values, close.values, close.values)

# test DIRECTIONAL MOVEMENT INDEX 
print Indicators.DX(close.values, close.values, close.values)
# print Indicators.BBANDS( series, timeperiod=20,
#                                  nbdevup=2.0, nbdevdn=2.0,
#                                  matype= TaLib.MA_EMA )

print Indicators.CDL2CROWS( close, close, close, close )                                 
print Indicators.CDL2CROWS( close, close, close, close )                                 
