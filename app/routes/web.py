from bson import ObjectId
from flask import Blueprint, redirect, url_for, request, render_template
from flask.json import jsonify
from flask_login import current_user, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired, Email, Length

import users.recommender as recommender
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
                user = User.create(form.email.data, form.password.data)
            except Exception as e:
                if str(e) == 'password_length':
                    return render_template('register.html', form=form,
                                           server_errors=['Your password should be between 8 and 20 characters long'])
                return render_template('register.html', form=form, server_errors=['An unexpected error occured'])

            login_user(user)
            return redirect(url_for('web.preferences'))
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
            # recommender.set_recommended_events(user.id)
            return redirect(url_for('web.dashboard'))

        return render_template('login.html', form=form, server_errors=['Wrong email or password!'])

    return render_template('login.html', form=form, server_errors=['Wrong email or password!'])


@web.route('/<category_id>/filter')
def filter_category(category_id):
    category = Category.objects.get(id=category_id)
    events = Event.objects(categories__in=[category])
    recommended = current_user.recommended_events
    return render_template('dashboard.html', name=current_user.email, events=events, recommended=recommended,
                           categories=current_user.categories, attending=current_user.events)


@web.route('/<event_id>/interested', methods=["POST"])
def record_interest(event_id):
    event = Event.objects.get(id=event_id)
    if event in current_user.events:
        current_user.update(pull_all__events=[event])
    else:
        current_user.update(add_to_set__events=[event])
    # user = User.objects(id=current_user.id).first()
    # recommender.set_recommended_events(user.id)
    # recommender.set_recommended_events(current_user.id)
    return redirect(request.referrer)


@web.route('/dashboard')
@login_required
def dashboard():
    user = User.objects(id=current_user.id).first()
    recommender.set_recommended_events(user.id)
    return render_template('dashboard.html', name=current_user.email)


@web.route('/user_events')
@login_required
def user_events():
    return to_json(current_user.events)


# TODO: make this show the recommended events!
@web.route('/user_recommended_events')
@login_required
def user_recommended_events():
    return to_json(current_user.recommended_events)


@web.route('/user_events/<event_id>', methods=["POST", "DELETE"])
@login_required
def edit_user_event(event_id):
    event_id = ObjectId(event_id)
    if request.method == 'POST':
        current_user.update(add_to_set__events=event_id)
    else:
        current_user.update(pull__events=event_id)

    return jsonify({})


@web.route('/events')
@login_required
def events():
    page_count = 24

    raw_page_num = request.args.get('page')
    page_num = 1
    if raw_page_num is not None and raw_page_num.isdigit() and int(raw_page_num) > 0:
        page_num = int(raw_page_num)

    raw_category_ids = request.args.get('category_ids')
    try:
        category_ids = raw_category_ids.split(',')
        category_ids = [ObjectId(cat_id) for cat_id in category_ids]
        events = Event.objects(categories__in=category_ids).skip((page_num - 1) * page_count).limit(page_count)
    except:
        events = Event.objects.skip((page_num - 1) * page_count).limit(page_count)

    return to_json(events)


@web.route('/user_categories')
@login_required
def user_categories():
    return to_json(current_user.categories)

def to_json(items):
    return jsonify([item.to_json() for item in items])


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
                               categories=[category.to_json() for category in all_categories],
                               user_category_ids=category_ids)

    form_string = request.form['categories']
    if form_string != '':
        raw_category_ids = form_string.split(',')
        category_ids = [ObjectId(category_id) for category_id in raw_category_ids]
        current_user.update(categories=category_ids)

    else:
        current_user.update(categories=None)

    # user = User.objects(id=current_user.id).first()
    # recommender.set_recommended_events(user.id)
    return redirect(url_for('web.dashboard'))
