'''
Define available options for each section
'''
CHART = [
    'chart',
    'colors',
    'credits',
    'global',
    'labels',
    'lang',
    'legend',
    'loading',
    'plotOptions',
    'point',
    'series',
    'subtitle',
    'symbols',
    'title',
    'tooltip',
    'xAxis',
    'yAxis',
    'rangeSelector',
    'scrollbar',
]


POINT = [
    'color',
    'id',
    'name',
    'sliced',
    'x',
    'y',
    'open',
    'high',
    'low',
    'close'
]


SERIES = [
    'allowPointSelect',
    'animation',
    'color',
    'cursor',
    'dashStyle',
    'data',
    'dataLabels',
    'enableMouseTracking',
    'id',
    'lineWidth',
    'name',
    'pointInterval',
    'pointStart',
    'selected',
    'shadow',
    'showCheckbox',
    'showInLegend',
    'stack',
    'stacking',
    'stickyTracking',
    'type',
    'visible',
    'xAxis',
    'yAxis',
    'zIndex'
]


# Config Sections
CHART_CONFIG = [
    'alignTickets',
    'animation',
    'backgroundColor',
    'borderColor',
    'borderRadius',
    'borderWidth',
    'className',
    'defaultSeriesType',
    'height',
    'ignoreHiddenSeries',
    'inverted',
    'margin',
    'marginTop',
    'marginRight',
    'marginBottom',
    'marginLeft',
    'plotBackgroundColor',
    'plotBackgroundImage',
    'plotBorderColor',
    'plotBorderWidth',
    'plotShadow',
    'reflow',
    'renderTo',
    'shadow',
    'showAxes',
    'spacingTop',
    'spacingRight',
    'spacingBottom',
    'spacingLeft',
    'style',
    'type',
    'width',
    'zoomType'
]


CREDITS_CONFIG = [
    'enabled',
    'position',
    'href',
    'style',
    'text'
]


SUBTITLE_CONFIG = [
    'align',
    'floating',
    'text',
    'style',
    'verticalAlign',
    'x',
    'y'
]


TITLE_CONFIG = SUBTITLE_CONFIG + [
    'margin'
]


LEGEND_CONFIG = [
    'align',
    'backgroundColor',
    'borderColor',
    'borderRadius',
    'borderWidth',
    'enabled',
    'floating',
    'itemHiddenStyle',
    'itemHoverStyle',
    'itemStyle',
    'itemWidth',
    'layout',
    'lineHeight',
    'margin',
    'reversed',
    'shadow',
    'style',
    'symbolPadding',
    'symbolWidth',
    'verticalAlign',
    'width',
    'x',
    'y'
]


TOOLTIP_CONFIG = [
    'backgroundColor',
    'borderColor',
    'borderRadius',
    'borderWidth',
    'crosshairs',
    'enabled',
    'shadow',
    'shared',
    'snap',
    'style'
]


X_AXIS_CONFIG = [
    'allowDecimals',
    'alternateGridColor',
    'categories',
    'dateTimeLabelFormats',
    'endOnTick',
    'gridLineColor',
    'gridLineDashStyle',
    'gridLineWidth',
    'id',
    'labels',
    'lineColor',
    'lineWidth',
    'linkedTo',
    'max',
    'maxPadding',
    'maxZoom',
    'min',
    'minorGridLineColor',
    'minorGridLineDashStyle',
    'minorGridLineWidth',
    'minorTickColor',
    'minorTickInterval',
    'minorTickLength',
    'minorTickPosition',
    'minorTickWidth',
    'minPadding',
    'offset',
    'opposite',
    'plotBands',
    'plotLines',
    'reversed',
    'showFirstLabel',
    'showLastLabel',
    'startOfWeek',
    'startOnTick',
    'tickColor',
    'tickInterval',
    'tickLength',
    'tickmarkPlacement',
    'tickPixelInterval',
    'tickPosition',
    'tickWidth',
    'title',
    'type',
    'range',
    'minRange',
]

Y_AXIS_CONFIG = [
    'top',
    'width',
    'height',
    'endOnTick',
    'gridLineWidth',
    'lineWidth',
    'maxPadding',
    'minPadding',
    'showLastLabel',
    'stackLabels',
    'startOnTick',
    'tickWidth',
    'allowDecimals',
    'alternateGridColor',
    'categories',
    'dateTimeLabelFormats',
    'gridLineColor',
    'gridLineDashStyle',
    'id',
    'labels',
    'lineColor',
    'linkedTo',
    'max',
    'maxZoom',
    'min',
    'minorGridLineColor',
    'minorGridLineDashStyle',
    'minorGridLineWidth',
    'minorTickColor',
    'minorTickInterval',
    'minorTickLength',
    'minorTickPosition',
    'minorTickWidth',
    'offset',
    'opposite',
    'plotBands',
    'plotLines',
    'reversed',
    'showFirstLabel',
    'startOfWeek',
    'tickColor',
    'tickInterval',
    'tickLength',
    'tickmarkPlacement',
    'tickPixelInterval',
    'tickPosition',
    'title',
    'type'
]

RANGE_SELECTOR_CONFIG = [
    'buttons',
    'buttonSpacing',
    'buttonTheme',
    'enabled',
    'inputBoxStyle',
    'inputDateFormat',
    'inputEditDateFormat',
    'inputEnabled',
    'inputStyle',
    'labelStyle',
    'selected',
]

MARKER_CONFIG = [
    'enabled',
    'fillColor',
    'lineColor',
    'lineWidth',
    'radius',
    'symbol',
]

SCROLLBAR_CONFIG = [
    'enabled',
    'height',
    'barBackgroundColor',
    'barBorderRadius',
    'barBorderWidth',
    'barBorderColor',
    'buttonArrowColor',
    'buttonBackgroundColor',
    'buttonBorderColor',
    'buttonBorderRadius',
    'buttonBorderWidth',
    'rifleColor',
    'trackBackgroundColor',
    'trackBorderColor',
    'trackBorderWidth',
    'trackBorderRadius'
]
