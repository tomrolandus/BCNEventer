from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('settings.cfg', silent=False)

mongo = PyMongo(app)


@app.route('/')
def index():
    return 'Hello, World!'
