# -*- coding: utf-8 -*-

from .views.api import Api

def setup_routes(app):
  """
  Registers :class:`flask.Blueprint` instances and adds routes all at once.

  :param app: The current application.
  :type app: flask.Flask.
  :param routes: The routes definition in the format:
      ((blueprint_instance, url_prefix),
          ('/route1/<param>', view_function1),
          ('/route2', view_function2),
          ...
      )
  :type routes: tuple.
  :returns: None
  """
  
  home = Api(app).configure_routes()

  