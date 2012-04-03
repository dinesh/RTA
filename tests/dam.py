
from datetime import date

from helper import rta
from rta import dam, config, model

db = model.MongoDB()
yahoodam = dam.YahooDAM()

''' Import one year data '''
yahoodam.importQuotes(db, date(2008, 1, 1), date(2009, 1, 1))


