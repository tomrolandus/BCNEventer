import json

from bson import ObjectId
from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import current_user, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired, Email, Length

from app.models.category import Category
from app.models.event import Event
from app.models.user import User

web = Blueprint('web', __name__, template_folder='/templates')


class RegForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])


@web.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('web.dashboard'))
    return redirect(url_for('web.login'))


@web.route('/register', methods=['GET', 'POST'])
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

            return redirect(url_for('web.dashboard'))
        return render_template('register.html', form=form, server_errors=['Your email is already registered!'])

    return render_template('register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = RegForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)

    if form.validate():
        user = User.objects(email=form.email.data).first()
        if user and user.login(form.password.data):
            login_user(user)
            return redirect(url_for('web.dashboard'))

        return render_template('login.html', form=form, server_errors=['Wrong email or password!'])

    return render_template('login.html', form=form, server_errors=['Wrong email or password!'])


@web.route('/dashboard')
@login_required
def dashboard():
    events = Event.objects
    recommended = []

    return render_template('dashboard.html', name=current_user.email, events=events, recommended=recommended,
                           categories=current_user.categories)


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.login'))


@web.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    if request.method == 'GET':
        all_categories = Category.objects
        category_ids = [str(category.id) for category in current_user.categories]

        return render_template('preferences.html', name=current_user.email,
                               categories=[category.as_json() for category in all_categories],
                               user_category_ids=category_ids)

    form_string = request.form['categories']
    if form_string != '':
        raw_category_ids = form_string.split(',')
        category_ids = [ObjectId(category_id) for category_id in raw_category_ids]
        current_user.update(categories=category_ids)
    else:
        current_user.update(categories=None)

    return redirect(url_for('web.dashboard'))
