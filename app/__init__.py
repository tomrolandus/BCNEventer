import os
from flask import Flask


def set_app_config(app):
    config = os.environ
    for key in config:
        if config[key] == 'True':
            app.config[key] = True
        elif config[key] == 'False':
            app.config[key] = False
        else:
            app.config[key] = config[key]


def create_app():
    from . import models, routes
    app = Flask(__name__)
    set_app_config(app)
    models.init_app(app)
    routes.init_app(app)
    return app
