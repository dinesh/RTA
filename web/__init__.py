# -*- coding: utf-8 -*-

from flask import Flask
import os
from web import settings
from .static import static_files
from .url import setup_routes

# setup application
current_dir = os.path.dirname(__file__)
app = Flask('rta', static_folder = os.path.join( current_dir, 'static') )
app.config.from_object(settings)

# register application views and blueprints
setup_routes(app)
