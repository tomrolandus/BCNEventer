# from flask_pymongo import PyMongo
from flask import Flask, render_template
from flask_mongoengine import MongoEngine
import csv
from .event import Event
from flask_login import LoginManager, login_required, current_user
import os
from .settings import APP_ROOT
from .auth.auth_controller import AuthController
app = Flask(__name__)

app.config.from_pyfile('../settings.cfg', silent=False)

app.config['MONGODB_SETTINGS'] = {
    'db': 'bcneventer',
    'host': 'mongodb://localhost:27017/bcneventer'
}
db = MongoEngine(app)
# mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

auth = AuthController()


@login_manager.user_loader
def load_user(user_id):
    return auth.load_user(user_id)


@app.route('/', methods=['GET'])
def index():
    return auth.route()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return auth.register()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth.login()


@app.route('/users-list', methods=['GET'])
def list_users():
    return auth.get_users()


@app.route('/dashboard')
@login_required
def dashboard():
    events = getEvents()
    return render_template('dashboard.html', name=current_user.email, events=events)


@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    return auth.logout()


def getEvents():
    events = []
    with open(os.path.join(APP_ROOT, 'static/events_Barcelona.csv'), 'rt') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            new_event = Event(row[3],(row[0],row[1]),row[2])
            events.append(new_event)
    return events
