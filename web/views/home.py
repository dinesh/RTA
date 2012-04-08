from flask import *
from flask.views import MethodView, View

import os
current_dir = os.path.dirname( os.path.abspath(__name__))

class HomeController(object):
  
  # templates, to override see get_template_overrides()
  base_templates = {
      'index': 'home/index.html',
  }
  
  def __init__(self, app, name = 'home', prefix = None):
    self.app = app
    self.blueprint = self.get_blueprint(name)
    self.url_prefix = prefix
    
  
  def get_blueprint(self, blueprint_name):
    return Blueprint(
        blueprint_name,
        __name__,
        template_folder= os.path.join(current_dir, 'web', 'templates'),
    )
  
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
      return render_template('home/index.html')

  
  def setup(self):
    self.configure_routes()
    self.register_blueprint()
    return self