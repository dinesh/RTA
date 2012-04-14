
class exports.MainRouter extends Backbone.Router
  routes:
    '': 'home'
  
  home: ->
    $('body #main').html app.homeView.render().el
