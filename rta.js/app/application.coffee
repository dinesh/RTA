
API = require('api')

window.api = new API()

{BrunchApplication} = require 'helpers'
{MainRouter} = require 'routers/main_router'
{HomeView} = require 'views/home'

Indicator = require('models/indicator')
Indicators = require('collections/indicators')


class Symbol extends Backbone.Model


class Symbols extends Backbone.Collection
  url: 'api/symbols.json'
  sync: api.sync
  model: Symbol
  parse: (json) ->
    _.map(json.records, (p) -> { 'name': '$' + p, 'id': p } )
    
class exports.Application extends BrunchApplication
  # This callback would be executed on document ready event.
  # If you have a big application, perhaps it's a good idea to
  # group things by their type e.g. `@views = {}; @views.home = new HomeView`.
  initialize: ->
    @router = new MainRouter
    @homeView = new HomeView
    @Indicators = new Indicators({ model: Indicator })
    @Indicator = Indicator
    @Symbol = Symbol
    @Symbols = new Symbols
    
window.app = new exports.Application
