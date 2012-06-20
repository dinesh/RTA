import encoders
import options
from .common import *
from config_sections import *
from series import *


class Chart(DictBacked):
    '''
    The base config for a highcharts chart.

    See http://www.highcharts.com/ref/ for available options.
    '''
    available_options = options.CHART
    defaults = {
        "series": [],
        "chart": ChartConfig,
        "credits": CreditsConfig,
        "title": TitleConfig,
        "subtitle": SubtitleConfig,
        "legend": LegendConfig,
        "tooltip": TooltipConfig,
        "xAxis": XAxisConfig,
        "yAxis": YAxisConfig,
        "rangeSelector": RangeSelectorConfig,
        "scrollbar": ScrollbarConfig,
    }

    def add_series(self, series, *args, **kwgs):
        if not isinstance(series, Series): 
          series = PDSeries(data=series, *args, **kwgs)
        self.series.append(series)
        
    def __str__(self):
        return encoders.dump_json(self)
