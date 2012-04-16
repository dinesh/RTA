
sidebarTmpl = require('views/templates/sidebar')
symbolTmpl = require('views/templates/symbols')

ChartView = require('views/chart')

class SidebarView extends Backbone.View
  tagName: 'ul'
  id: 'side-inds-list'
  className: 'list'
  
  events:
    'click .add' : 'addIndicator'
    
  initialize: ->
    super()
    @container = this.options.container
    @collection.bind('reset', @render).fetch()
    
  render: =>
    $(@el).html( sidebarTmpl( 'items' : @collection.models ))
    @container.html( @el )  
    @
  
  addIndicator: (ev) =>
    target = this.$(ev.currentTarget)
    indicator = @collection.get( target.data('id') )
    
    unfilled = _.map indicator.get('args'), (opt) ->
      name = "#{indicator.get('id')}[#{ opt }]"
      val = $("[name='" + name +  "']" ).val() 
      _.isEmpty(val)
    
      
    if unfilled and false
      $(target).closest('li').addClass('alert alert-error')
      return false
      
    if ( symbol = app.ui.companyDp.selectedValue() ) and app.models.chart
      range = app.models.chart.dateRange()
      url = [ api.url, indicator.url(), symbol, 'series.json' ].join('/')
      
      $.ajax 
        url: url
        dataType: 'jsonp',
        data:
          start: range.dataMin
          end: range.dataMax
        success: (data) ->
          console.log data
          app.models.chart.addSeries indicator.get('name'), data.records,
            yAxis : 0
          
    else
      alert('No Symbol selected.')
       
class SymbolListView extends Backbone.View
  tagName: 'select'
  
  initialize: ->
    super()
    @container = this.options.container
    @collection.bind('reset', @render).fetch()
    
  render: =>
    $(@el).html( symbolTmpl( 'items' : @collection.models ))
    @container.append( @el )  
    @
  
  selectedValue: =>
    $(@el).val()
    
class exports.HomeView extends Backbone.View
  
  className: 'container'
  events:
    'change #symbol-list select': 'openChart'
      
  render: =>
    $(@el).html require('./templates/home')
    @subviews = [
      new SidebarView( 'collection': app.Indicators, 'container': @.$('#sidebar') ) 
      app.ui.companyDp = new SymbolListView( 'collection': app.Symbols, 'container': @.$('#symbol-list') )
    ]
    @
  
  openChart: (ev) =>
    model = app.Symbols.get( @.$(ev.currentTarget).val() )
    @currentChart = new ChartView( 'model': model, 'el' : @.$('#chart').get(0) )
    # app.ui.chartview = @currentChart
    @subviews.push( @currentChart.render() )
    @
      