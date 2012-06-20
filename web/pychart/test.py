
import numpy as np
import pandas as pd
import highcharts

chart = highcharts.Chart()
series = highcharts.TimeSeries( data = pd.Series( np.random.randint(-100, 100, size = 100) ) )
chart.add_series(series)

ohlc = highcharts.OHLCSeries( data = pd.DataFrame({ 
                              'open'  : np.random.randint(-100, 100, size = 20 ), 
                              'high'  : np.random.randint(-100, 100, size = 20 ),
                              'low'   : np.random.randint(-100, 100, size = 20 ),
                              'close' : np.random.randint(-100, 100, size = 20 )
                            } ))
                            
chart.add_series( ohlc )

buy_flags = highcharts.FlagSeries('Buy', data = pd.Series(np.random.randint(0, 100, size = 10) ) )
sell_flags = highcharts.FlagSeries('Sell', data = pd.Series(np.random.randint(0, 100, size = 10) ) )

chart.add_series( buy_flags )
chart.add_series( sell_flags )

print chart