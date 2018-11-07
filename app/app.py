# from flask_pymongo import PyMongo
from flask import Flask, render_template

from flask import request, redirect, url_for

from flask_mongoengine import MongoEngine

import csv
from .event import Event

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from .auth.registration_form import RegForm
# from .auth.user import User
from werkzeug.security import generate_password_hash, check_password_hash


import os
from .settings import APP_ROOT
from .auth.auth_controller import AuthController
app = Flask(__name__)

app.config.from_pyfile('../settings.cfg', silent=False)

# app.config['MONGO_DBNAME'] = 'bcneventer'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/bcneventer'
app.config['MONGODB_SETTINGS'] = {
    'db': 'bcneventer',
    'host': 'mongodb://localhost:27017/bcneventer'
}
db = MongoEngine(app)
#mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

auth = AuthController()

# class User(UserMixin, db.Document):
#     meta = {'collection': 'users'}
#     email = db.StringField()
#     password = db.StringField()
#
#     def __repr__(self):
#         return 'emaily: '+self.email+', password: '+self.password
#
#     def __str__(self):
#         return 'my str'


@login_manager.user_loader
def load_user(user_id):
    return auth.load_user(user_id)

    # return User.objects(pk=user_id).first()


@app.route('/', methods=['GET'])
def index():
    return auth.route()
    # if current_user.is_authenticated == True:
    #     return redirect(url_for('dashboard'))
    # return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    return auth.register()
    # form = RegForm()
    # if request.method == 'POST':
    #
    #     if form.validate():
    #         existing_user = User.objects(email=form.email.data).first()
    #         if existing_user is None:
    #             hashpass = generate_password_hash(form.password.data, method='sha256')
    #             # return form.email+'   '+hashpass
    #             hey = User(form.email.data,hashpass).save()
    #             login_user(hey)
    #             return redirect(url_for('dashboard'))
    #         else:
    #             return render_template('register.html', form=form, server_errors=['Your email is already registered!'])
    # return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth.login()
    # if current_user.is_authenticated == True:
    #     return redirect(url_for('dashboard'))
    # form = RegForm()
    # if request.method == 'POST':
    #     if form.validate():
    #         check_user = User.objects(email=form.email.data).first()
    #         if check_user:
    #             if check_password_hash(check_user['password'], form.password.data):
    #                 login_user(check_user)
    #                 return redirect(url_for('dashboard'))
    #             else:
    #                 return render_template('login.html', form=form, server_errors=['Wrong email or password!'])
    #         else:
    #             return render_template('login.html', form=form, server_errors=['Wrong email or password!'])
    #     else:
    #         return render_template('login.html', form=form, server_errors=['Wrong email or password!'])
    # return render_template('login.html', form=form)

@app.route('/test', methods=['GET'])
def test():
    # hey = User("webmaster.sy@gmail.com", "123").save()
    hey = User.objects().all()
    check_me = hey
    if check_me:
        return repr(check_me)
    return 'Not found!'

@app.route('/dashboard')
@login_required
def dashboard():
    events = getEvents()
    return render_template('dashboard.html', name=current_user.email, events=events)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    return auth.logout()
    # logout_user()
    # return redirect(url_for('login'))



def getEvents():
    events = []
    with open(os.path.join(APP_ROOT, 'static/events_Barcelona.csv'), 'rt') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            new_event = Event(row[3],(row[0],row[1]),row[2])
            events.append(new_event)
    return events
