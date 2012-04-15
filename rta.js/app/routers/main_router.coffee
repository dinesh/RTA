
class exports.MainRouter extends Backbone.Router
  routes:
    '': 'home'
  
  home: ->
    $('body #main').html ( app.ui.homeview = app.homeView.render() ).el
