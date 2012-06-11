
import os, sys
import pandas 

sys.path.append( os.path.join( os.path.dirname( os.path.abspath(__file__) ), '..' ) )
series = pandas.read_csv('tests/table.csv')


from rta import api as CoreApi
from rta import indicators as IND


