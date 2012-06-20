
HEIGHTS = { 'overlay': 500 , 'top': 100, 'bottom': 100, 'margin': 10 }
OV_HEIGHT = HEIGHTS['overlay']
PS_HEIGHT = HEIGHTS['top']
MARGIN = HEIGHTS['margin']

class StockChart
  constructor: (@el, @title, options) ->
    $(@el).css({ 'min-height': '685px'})
    
    @options = options || {}
    
    @items = 
      'overlay': []
      'top': [],
      'bottom': []
    
    self = this
    
    app.chart = @handle = new Highcharts.StockChart
      chart:
        alignTicks : false
        renderTo : @el
      title:
        text: @title
      rangeSelector: @rangeSelector()
      navigator: 
        enabled: true
      series: options.series || []
      xAxis:
        type: 'date'
        zoomType: 'x'
        
      yAxis: [ {  
        title:
          text: 'OHLC'
        height: 300
        }, {
        title:
          text: 'Volume'
        height: 75
        top: 365
        offset: 0,
        }, {
          title:
            text: 'Indicator'
          height: 150
          top: 440
          opposite: true
        }]
      , (_chart) ->
        
        # apply the date pickers
        setTimeout () ->
          $('input.highcharts-range-selector', $( _chart.options.chart.renderTo )).datepicker
            format: 'dd-mm-yyyy',
          .on('changeDate', self.onChangeDate )      
        , 0
      
  addSeries: (name, series, options) =>
    position = options['position' ] || 'overlay'
    @items[position].push(name)    
    s = @handle.addSeries _.extend 
      name: name
      data: series
    , options
    
    if options['redraw']
      @handle.redraw()
      
    s
    
  dateRange: =>
	  @handle.xAxis[0].getExtremes()
  
  rangeSelector: =>
  	sel =
  	  selected : 1
  	  inputDateFormat: '%d-%m-%Y'
  	  inputEditDateFormat: '%d-%m-%Y'
      
  onChangeDate: (ev) =>
    selectedDate = ev.date
    option = this.name == "min" ? "minDate" : "maxDate"
    instance = $( this ).data( "datepicker" )
    
    startDate = $("input[name='min']")[0].value
    endDate   = $("input[name='max']")[0].value
    
    if startDate != "" && endDate != ""
        startDate = startDate.split("-")
        endDate   = endDate.split("-")
        sd  = new Date( Date.UTC(startDate[2], startDate[1]-1, startDate[0]) )
        ed  = new Date( Date.UTC(endDate[2], endDate[1]-1, endDate[0]) )
        @handle.xAxis[0].setExtremes(sd, ed)
	
class ChartView extends Backbone.View
  className: 'chart'
  
  render: =>
    url = [ api.url, 'api/quotes',  @model.get('id') + '.json?flush=true' ].join('/')
    $.getJSON url + '&callback=?', (data) =>
      @stockchart = new StockChart(@el, @model.get('id'), data.chartjson)
      app.models.chart = @stockchart
    		 
    @
  

module.exports = ChartView
