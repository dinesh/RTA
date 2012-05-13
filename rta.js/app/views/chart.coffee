
HEIGHTS = { 'overlay': 500 , 'top': 100, 'bottom': 100, 'margin': 10 }
OV_HEIGHT = HEIGHTS['overlay']
PS_HEIGHT = HEIGHTS['top']
MARGIN = HEIGHTS['margin']

class StockChart
  constructor: (@el, @title, options) ->
    $(@el).css({ 'min-height': '1000px'})
    
    @options = options || {}
    
    @items = 
      'overlay': []
      'top': [],
      'bottom': []
    
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
        height: 100
        top: 800
        offset: 0,
        }, {
          title:
            text: 'Indicator'
          height: 300
          top: 400
          opposite: true
        }]
      
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
  	selected : 1,
		
	  
	
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
          opposite: true
          }]
    
      app.models.chart = @stockchart
    		 
    @
  

module.exports = ChartView