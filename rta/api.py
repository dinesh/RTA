

# this file would be used to interface this library with other system
# import all things here and other can use it

# site-packages
import os, dateutil, sys, time
from matplotlib import finance as matplotlib_finance
import urllib2

import pandas
import numpy as np
import mongokit # mongokit is minimal ORM fast based on execellent pymongo


# rta packages
from rta import indicators as Indicators 
from rta.indicators import talib as TaLib
from rta.indicators import (
        LIST, 
        IndicatorBase, 
        IndicatorFactory,
        bbands, cci, macd, rsi, zigzag, accept_ohlc, accept_hlc_timeperiod, accept_ohlc_penetration
      )

from rta import model as Model
from rta import ts as TS
from rta.configuration import Config
from rta import configuration as Configuration
from rta.dam import YahooDAM
from rta.errors import UfException, Errors
from .common import *

# logger
import logging
LOG = logging.getLogger()

# coul't able to make it work
# Indicators.register_indicators()