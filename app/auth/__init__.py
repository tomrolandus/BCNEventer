from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_pyfile('../../settings.cfg', silent=False)

db = MongoEngine(app)

