
Indicator = require('models/indicator')

class Indicators extends Backbone.Collection
  url: 'api/indicators'
  sync: api.sync
  model: Indicator
  
  parse: (json) ->
    _.map(json.indicators, (p) -> p )
  
  validKeys :() ->
    ['timeperiod', 'matype', 'nbdevdn', 'nbdevup', 'matype', 'slowk_matype', 'slowd_matype', 'fastd_matype' ]
    
module.exports = Indicators  
  