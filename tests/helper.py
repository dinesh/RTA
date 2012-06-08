
import os, sys
import pandas 

sys.path.append( os.path.join( os.path.dirname( os.path.abspath(__file__) ), '..' ) )
series = pandas.read_csv('./601398.csv')

