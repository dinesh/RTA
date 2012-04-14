
class ChartView extends Backbone.View
  className: 'chart'
    
  constructor: ->
    @symbol = this.options.symbol
    
  render: =>
    url = [ api.url, '/qoutes/' + @symbol + '.json?fields=open,high,close,low,ticker' ].join('/')
    
    $.getJSON url + '&callback=?', (data) =>
    		# create the chart
    		chart = new Highcharts.StockChart
    			chart : 
    				renderTo : @el
    			
    			title: 
    				text: @options.text || 'AAPL stock price by minute'
    		  
    		  rangeSelector: @rangeSelector()
    		  
    			series : [{
    				name : @options['symbol'],
    				type: @options['type'] || 'candlestick',
    				data : data.records,
    				tooltip: {
    					valueDecimals: 2
    				}
    			}]
    			
  rangeSelector: =>
  	buttons : [
  	  { type : 'hour', count : 1, text : '1h' }, 
  	  { type : 'day', count : 1, text : '1D'}, 
  	  { type : 'all', count : 1, text : 'All' } ],
		selected : 1,
		inputEnabled : false

module.exports = ChartView