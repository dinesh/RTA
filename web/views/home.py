from flask import *
from flask.views import MethodView, View
from flaskext.wtf import Form, TextField, Required, SelectField

import os
current_dir = os.path.dirname( os.path.abspath(__name__))
from rta import api as API

class IndicatorForm(Form):
  indicator = SelectField()
  
class HomeHelper(object):
  def __init__( self, home ):
    self.home = home
    self.app = home.app
  
  def get_indicators(self):
    d = API.ALL_INDICATORS
    return dict((i, d[i]) for i in API.SUPPORTED_INDICATORS )
    
  def prepare_env(self):
    self.app.jinja_env.globals['indicators'] = self.get_indicators()
   
  
class HomeController(object):
  
  # templates, to override see get_template_overrides()
  base_templates = {
      'index': 'home/index.html',
  }
  
  def __init__(self, app, name = 'home', template_helper = HomeHelper , prefix = None):
    self.app = app
    self.blueprint = self.get_blueprint(name)
    self.url_prefix = prefix
    
    self.template_helper = template_helper(self)
    self.template_helper.prepare_env()
    
    # print self.template_helper.get_indicators()
    
  def get_blueprint(self, blueprint_name):
    return Blueprint(
        blueprint_name,
        __name__,
        template_folder= os.path.join(current_dir, 'web', 'templates'),
    )
  
  def indicators(self):
    pass
  def get_urls(self):
      return (
          ('/', self.index),
          # ('/add/', self.add),
          # ('/delete/', self.delete),
          # ('/export/', self.export),
          # ('/<pk>/', self.edit),
          # ('/_ajax/', self.ajax_list),
      )

  def configure_routes(self):
    for url, callback in self.get_urls():
      self.blueprint.route(url, methods=['GET', 'POST'])(callback)    
  
  def register_blueprint(self, **kwargs):
    self.app.register_blueprint(
        self.blueprint,
        url_prefix=self.url_prefix,
        **kwargs
    )
    
  def index(self):
    form = IndicatorForm()
    return render_template('home/index.html', indicatorForm = form )

  
  def setup(self):
    self.configure_routes()
    self.register_blueprint()
    return self