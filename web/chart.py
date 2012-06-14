
from pychart import highchart


class Chart(highchart.chart):
  available_options = [ 'symbol', 'start_date', 'end_date' ]
  
  def add_symbol(self, symbol, start_date, end_date):
    self.symbol = symbol
    self.start_date, self.end_date = start_date, end_date
    
    
  def add_indicator(self, indicator, **kwgs):
    pass