
# the basic class used for accessing data from python api
# overrides the Backbone.sync to do jsonp requests

class API 
  constructor: (options) ->
    options ||= {}
    @url = options['url'] || 'http://localhost:5000'
    
  setUrl: (url) =>
    @url = url
    
  sync : (method, model, options) =>
    options.timeout = 10000; # required, or the application won't pick up on 404 responses
    options.dataType = "jsonp";
    options.url = [ @url, options['url'] || model.url ].join('/')
    Backbone.sync(method, model, options);

module.exports = API