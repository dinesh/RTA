

class Indicator extends Backbone.Model
  url: 'api/indicator'
  sync: api.sync
  
  fullname: =>
    "#{ get('id') } - #{ get('desc') }"


module.exports = Indicator