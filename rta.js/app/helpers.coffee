

class exports.BrunchApplication
  constructor: ->
    $ =>
      @initialize this
      Backbone.history.start()

  initialize: ->
    
    # Set the datepicker's date format
    $.datepicker.setDefaults 
        dateFormat: 'yy-mm-dd'
        onSelect: (dateText) ->
            this.onchange()
            this.onblur()

