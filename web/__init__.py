# -*- coding: utf-8 -*-

from flask import Flask

from web import settings
from .static import static_files
from .url import setup_routing

# setup application
app = Flask('rta')
app.config.from_object(settings)

# register application views and blueprints
from shorty.urls import Routes
setup_routing(app, Routes)

# register context processors
app.context_processor(static_files)
