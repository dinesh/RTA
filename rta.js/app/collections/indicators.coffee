
class Indicators extends Backbone.Collection
  url: 'api/indicators'
  sync: api.sync
  
  parse: (json) ->
    _.map(json.indicators, (p) -> p )
       
  

module.exports = Indicators  
  