
class ChartView extends Backbone.View
  className: 'chart'
    
  render: =>
    url = [ api.url, 'api/quotes',  @model.get('id') + '.json?' ].join('/')
    that = @
    $.getJSON url + '&callback=?', (data) =>
    		# create the chart
    		chart = new Highcharts.StockChart
    		  chart:
    		    alignTicks : false
    		    renderTo : that.el
            
          title:
            text: @options.text || ( @model.get('name') + ' stock price by day' )
            
    		  rangeSelector: @rangeSelector()
    		  
    		  series : [{ 
    				name : 'OHLC',
    				type: @options['type'] || 'candlestick',
    				data : data.records,
    				tooltip: {
    					valueDecimals: 2
    				} }, {
    			  name: "Volume",
    			  type : 'column',
    			  data : data.volume }]
    
    @
    			
  rangeSelector: =>
  	buttons : [
  	  { type : 'day', count : 1, text : '1D'}, 
  	  { type : 'week', count : 1, text : '7D'}, 
      { type : 'all', count : 1, text : 'All' } ],
		selected : 1,
		inputEnabled : false

module.exports = ChartView