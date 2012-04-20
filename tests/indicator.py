
import helper
from datetime import datetime, timedelta
from rta.api import *

# mi = Configuration.indicator_by_rating(5)
# print mi

today = datetime.today()

prices = Model.Quote.series('3MINDIA', today - timedelta(days=100))
o = prices['open'].values
h = prices['high'].values
l = prices['low'].values
c = prices['close'].values
print prices.index.shape
print "*******************"


# test ADX
# pivot, res = Indicators.ADX(h, l, c, 30)
# 
# print prices.index.shape
# print pivot, res.shape

# test ADX
# pivot, res = Indicators.ADXR(close.values, close.values, close.values, 20)
# (0, [])

# test AVGPRICE
pivot, res =  Indicators.AVGPRICE(o,h,l,c)

print pivot
print prices.index.shape, res.shape



# test BBANDS
# pivot, res, res2, res3 =  Indicators.BBANDS( close.values, timeperiod=20,
#                                  nbdevup=2.0, nbdevdn=2.0,
#                                  matype= TaLib.MA_EMA )
                                 
# (19,) (39,) (39,) (39,)


# test CCI
# 
# pivot, res =  Indicators.CCI(close.values, close.values, close.values, 30)

# pivot, res = Indicators.CDL2CROWS(o,h,l,c)
# print pivot, res.shape

# pivot, res = Indicators.CDL3BLACKCROWS(o,h,l,c)
# print pivot, res.shape

# pivot, res = Indicators.CDL3WHITESOLDIERS(o,h,l,c)
# print pivot, res.shape, res

# pivot, res = Indicators.CDLDARKCLOUDCOVER(o,h,l,c, 100)
# print pivot, res.shape, res
# 
# pivot, res = Indicators.CDLDOJI(o,h,l,c)
# print pivot, res.shape, res

# pivot, res = Indicators.CDLDRAGONFLYDOJI(o,h,l,c)
# print pivot, res.shape, res

# pivot, res = Indicators.CDLEVENINGDOJISTAR(o,h,l,c, 100)
# print pivot, res.shape, res
# 
# pivot, res = Indicators.CDLEVENINGSTAR(o,h,l,c, 100)
# print pivot, res.shape, res


# pivot, res = Indicators.CDLGRAVESTONEDOJI(o,h,l,c)
# print pivot, res.shape, res

# 
# pivot, res = Indicators.CDLHAMMER(o,h,l,c)
# print pivot, res.shape, res
# 
# pivot, res = Indicators.CDLHANGINGMAN(o,h,l,c)
# print pivot, res.shape, res


# pivot, res = Indicators.DX(h,l,c, 30)
# print pivot, res.shape, res
# 

# 
# pivot, res = Indicators.HT_TRENDLINE(c)
# print pivot, res.shape, res

# 
# pivot, res, res2, res3 = Indicators.MACD(c, 10, 30, 5)
# print pivot, res.shape, res2.shape, res3.shape


# 
# pivot, res = Indicators.MAX(c,5)
# print pivot, res.shape, res
# 
# pivot, res = Indicators.MINUS_DI(h, l, c,10)
# print pivot, res.shape, res










