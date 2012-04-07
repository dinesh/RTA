
import helper
from datetime import datetime, timedelta
from rta.api import *

today = datetime.today()

closeSeries = Model.Quote.series('3MINDIA', today - timedelta(days=100))['close']

Indicators.SMA(closeSeries.value)
