
import pandas as pd
import numpy as np

class Above:
  __slots__ = ['first', 'second']
  
  def __init__(self, first, second):
    self.first = first
    self.second = second
  
  def detect(self):
    return self.first[ self.first > self.second ]
    
    