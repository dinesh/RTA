
from datetime import date
import helper
from rta.api import *

db = Model.MongoDB()
yahoodam = YahooDAM()

''' Import 1 year data '''
yahoodam.importQuotes(db, date(2010, 1, 1), date(2012, 12, 20))


