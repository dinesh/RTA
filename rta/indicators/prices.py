

import numpy as np
import pandas as pd

from . import IndicatorBase, IndicatorFactory
from rta import common

class Prices:
  
  def __init__(self, series):
    self.series = series
    
  def calculate(self, eodtype):
    return self.series[eodtype]