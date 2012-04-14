
app.ui.spinner = 
  
  show : (message) ->
    this.ensureElement();
    message = message || "Loading";
    this.el.stop(true, true).fadeIn('fast');
  
  hide : () ->
    this.ensureElement()
    this.el.stop(true, true).fadeOut('fast', ()->  $(this).css({display : 'none'}) )
  
  ensureElement : () ->
    this.el || (this.el = $('#spinner'))
  
_.bindAll(app.ui.spinner, 'show', 'hide')