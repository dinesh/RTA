
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
    
class exports.HomeView extends Backbone.View
  
  className: 'container'
  events:
    'change #symbol-list select': 'openChart'
      
  render: =>
    $(@el).html require('./templates/home')
    @subviews = [
      new SidebarView( 'collection': app.Indicators, 'container': @.$('#sidebar') ) 
      new SymbolListView( 'collection': app.Symbols, 'container': @.$('#symbol-list') )
    ]
    @
  
  openChart: (ev) =>
    model = app.Symbols.get( @.$(ev.currentTarget).val() )
    @currentChart = new ChartView( 'model': model, 'el' : @.$('#chart').get(0) )
    @subviews.push( @currentChart.render() )
    @
      