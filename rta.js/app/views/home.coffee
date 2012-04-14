
sidebarTmpl = require('views/templates/sidebar')


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
    @container.append( @el )  
    @
  
  addIndicator: (ev) =>
    target = this.$(ev.currentTarget)
    indicator = @collection.get( target.data('id') )
    
class exports.HomeView extends Backbone.View
  
  className: 'container'
    
  render: =>
    $(@el).html require('./templates/home')
    new SidebarView( 'collection': app.Indicators, 'container': @.$('#sidebar') ) 
    @
    