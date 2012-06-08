
import helper
from datetime import datetime, timedelta
from rta.api import *


today = datetime.today()

prices = Model.Quote.series('3MINDIA', today - timedelta(days=300))

o = prices['open'].values
h = prices['high'].values
l = prices['low'].values
c = prices['close'].values
