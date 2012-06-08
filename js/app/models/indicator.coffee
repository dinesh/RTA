

class Indicator extends Backbone.Model
  url: 'api/indicator'
  sync: api.sync
  
  fullname: =>
    "#{ this.id } - #{ this.get('desc') }"
    
  removeFromChart: =>
    if @charts.length > 0
      _.each( @charts, (series) -> series.remove() )
      @charts = []
    @
      
  addToChart: (options, callback) =>
    
    @charts ||= []
    this.removeFromChart()
      
    if ( symbol = app.ui.companyDp.selectedValue() ) and app.models.chart
      range = app.models.chart.dateRange()
      _url = [ api.url, this.collection.url, this.id, symbol, 'series.json' ].join('/')
      
      data = 
        start: range.dataMin
        end: range.dataMax

      _.each(options, (e) -> data[ e[0]] = e[1].val() )

      $.ajax 
        url: _url
        dataType: 'jsonp',
        data: data
        success: (data) =>
          
          streams = data.records
          settings = data.settings
          
          _.each streams, (ts) =>
            yaxis = parseInt( if _.isUndefined(ts.position) then 2 else ts.position )
            @charts.push( app.models.chart.addSeries ts.name, ts.series, { yAxis : yaxis, id: ts.name, 'type': ts.type || 'line' } )
            
            if ts.flags
              params = 
                onSeries: ts.name,
                yAxis : yaxis,
                type: 'flags'   
                width: 25
                shape: 'circlepin'

              _.each ts.flags, ( list, title ) =>
                @charts.push( app.models.chart.addSeries ts.name + "-#{title}", _.map( list, (e) -> { x: e, title: title }), params )

          callback(settings) if callback      

module.exports = Indicator