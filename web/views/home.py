from flask import *
from flask.views import MethodView, View

homeController = Blueprint('home', __name__)


class IndexView(MethodView):
    template = 'home/index.html'

    def get(self):
        return "Hello World"
