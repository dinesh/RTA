#!/usr/bin/env python

import os , sys
import optparse
from datetime import date
from dateutil import parser as dtparser

sys.path.append( os.path.join( os.path.dirname( os.path.abspath(__file__) ), '..' ) )

from rta import api

def main():
  parser = optparse.OptionParser(usage="usage: %prog [options] filename", version="%prog 1.0")
  
  parser.add_option('-n', '--symbol', help='The stock symbol')
  parser.add_option('-s', '--start-date', help='start date in %y-%m-%d', default='1 Jan')
  parser.add_option('-e', '--end-date', help='end datein %y-%m-%d', default = '30 Dec')
  parser.add_option('-d', '--delete', help='delete the symbol entries')
  parser.add_option('-l', '--list', help='list the symbols matching regexp')
  parser.add_option('-u', '--update', action='store_true', help='update the symbol data')
  
  (options, args) = parser.parse_args()
  allitems = api.Config['symbols']
  
  if options.list:
    ftlist = allitems[ allitems.map( lambda x: x.lower().startswith(options.list) ) ]
    print ftlist
  
  if options.symbol:
    item = allitems[ allitems.map( lambda x: x == options.symbol ) ]
    if item.size < 1:
      parser.error("not able to find %s symbol in the database" % options.symbol)
    
    if options.start_date:
      start_date = dtparser.parse( options.start_date )
    if options.end_date:
      end_date = dtparser.parse( options.end_date )
    db = api.Model.MongoDB()
    yahoodam = api.YahooDAM()
    yahoodam.importQuotes(db, start_date, end_date, symbols = [ options.symbol ] )

if __name__ == '__main__':
  main()
