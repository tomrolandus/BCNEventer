import csv
import os
from urllib.parse import urlparse, urljoin

from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import login_required, login_user, user_logged_in, current_user, LoginManager, logout_user
from flask_mongoengine import MongoEngine

from app.User import User
from app.auth.registration_form import RegForm
from .event import Event
from .settings import APP_ROOT

app = Flask(__name__)
app.config.from_pyfile('../settings.cfg', silent=False)
db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    if user_id == 'None':
        return None

    return User.objects(pk=user_id).first()


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()

    if request.method == 'POST' and form.validate():
        user = User.objects(email=form.email.data).first()
        if user is None:
            try:
                User.create(form.email.data, form.password.data)
            except Exception as e:
                if str(e) == 'password_length':
                    return render_template('register.html', form=form,
                                           server_errors=['Your password should be between 8 and 20 characters long'])
                return render_template('register.html', form=form, server_errors=['An unexpected error occured'])

            return redirect(url_for('dashboard'))
        return render_template('register.html', form=form, server_errors=['Your email is already registered!'])

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)

    if form.validate():
        user = User.objects(email=form.email.data).first()
        if user and user.login(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))

        return render_template('login.html', form=form, server_errors=['Wrong email or password!'])

    return render_template('login.html', form=form, server_errors=['Wrong email or password!'])


@app.route('/dashboard')
@login_required
def dashboard():
    events = get_events()
    return render_template('dashboard.html', name=current_user.email, events=events)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def get_events():
    events = []
    with open(os.path.join(APP_ROOT, 'static/events_Barcelona.csv'), 'rt') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            new_event = Event(row[3], (row[0], row[1]), row[2])
            events.append(new_event)
    return events
