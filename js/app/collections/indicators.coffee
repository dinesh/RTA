
Indicator = require('models/indicator')

class Indicators extends Backbone.Collection
  url: 'api/indicators'
  sync: api.sync
  model: Indicator
  
  parse: (json) ->
    _.map(json.indicators, (p) -> p )
  
  validKeys :() ->
    # should get by api TODO
    [ 'timeperiod', 'matype', 'nbdevdn', 'nbdevup', 'matype', 
      'slowk_matype', 'slowd_matype', 'fastd_matype', 'cutoff', 
      'fastperiod', 'slowperiod', 'signalperiod', 'numlines'
     ]
    
module.exports = Indicators  
  