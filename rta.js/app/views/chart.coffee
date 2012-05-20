
HEIGHTS = { 'overlay': 500 , 'top': 100, 'bottom': 100, 'margin': 10 }
OV_HEIGHT = HEIGHTS['overlay']
PS_HEIGHT = HEIGHTS['top']
MARGIN = HEIGHTS['margin']

class StockChart
  constructor: (@el, @title, options) ->
    $(@el).css({ 'min-height': '900px'})
    
    @options = options || {}
    
    @items = 
      'overlay': []
      'top': [],
      'bottom': []
    
    self = this
    
    @handle = new Highcharts.StockChart
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
        height: 150
        top: 600
        offset: 0,
        }, {
          title:
            text: 'Indicator'
          height: 300
          top: 400
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
    url = [ api.url, 'api/quotes',  @model.get('id') + '.json?' ].join('/')
    
    
    $.getJSON url + '&callback=?', (data) =>
      @stockchart = new StockChart @el, @model.get('id'),
        series: [{
          name: 'OHLV', 
          data: data.records, 
          type : 'line',
          }, {
          name: 'Volume', 
          data: data.volume
          type : 'column'
          yAxis: 1 
          }, {
          name : 'Trendline',
          data: data.trendline,
          type: 'line'
          }]
    
      app.models.chart = @stockchart
    		 
    @
  

module.exports = ChartView