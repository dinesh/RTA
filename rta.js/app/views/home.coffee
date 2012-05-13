
sidebarTmpl             = require('views/templates/sidebar')
symbolTmpl              = require('views/templates/symbols')
indicatorFormViewTempl  = require('views/templates/indicator_form')

ChartView = require('views/chart')

class IndicatorFormView extends Backbone.View
  tagName: 'li'
  
  initialize: ->
    super()
    @model = this.options.model
    
  render: =>
    $(@el).attr('data-id', "ind-#{@model.id}").html( indicatorFormViewTempl(item: @model ) )
    @
    
class SidebarView extends Backbone.View
  events:
    'change select' : 'addIndicatorwithDefault'
    'click input.edit': 'addIndicator'
        
  initialize: ->
    super()
    @collection.bind('reset', @render).fetch()
    
  render: =>
    $(@el).html( sidebarTmpl('items' : @collection.models ) )
    @
  
  addIndicatorwithDefault: (ev) =>
    target = $(ev.currentTarget, @el)
    indicator = @collection.get( target.val() )
    if indicator
      this._addIndicator(indicator, {})    
    @
      
  addIndicator: (ev) =>
    target = $(ev.currentTarget, @el)
    indicator = @collection.get( $(target).data('id') )
    
    indicator_options = _.map indicator.get('args'), (opt) ->
      name = "#{indicator.get('id')}[#{ opt }]"
      elem = $("[name='" + name +  "']" )
      [ opt, elem ]
      
    unfilled = _.any(indicator_options, (p) -> _.isEmpty(p[1].val() ) )     
    
    if unfilled 
      $(target).closest('li').addClass('alert alert-error')
      return false
    
    this._addIndicator(indicator, indicator_options)
    @
    
  _addIndicator: (indicator, inputs) =>  
    that = this
    callback = (params) ->
      options = _.pick( params, that.collection.validKeys() )
      indicator.settings = options
      list = $('#side-inds-list', that.el )
      if $("li[data-id='ind-#{indicator.id}']", list).length < 1
        list.append( new IndicatorFormView( model: indicator ).render().el )
      
    if ( symbol = app.ui.companyDp.selectedValue() ) and app.models.chart
      indicator.addToChart( inputs, callback )
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
    $('#topbar').html require('./templates/header')
    
    @subviews = [
      new SidebarView( 'collection': app.Indicators, 'el': @.$('#sidebar') ) 
      app.ui.companyDp = new SymbolListView( 'collection': app.Symbols, 'container': @.$('#symbol-list') )
    ]
    @
  
  openChart: (ev) =>
    model = app.Symbols.get( @.$(ev.currentTarget).val() )
    @currentChart = new ChartView( 'model': model, 'el' : @.$('#chart').get(0) )
    @subviews.push( @currentChart.render() )
    @
      