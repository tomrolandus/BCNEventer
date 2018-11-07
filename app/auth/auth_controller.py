from flask import Flask, render_template

from flask import request, redirect, url_for

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from .registration_form import RegForm
from werkzeug.security import generate_password_hash, check_password_hash
from .user import User


class AuthController:

    user = None

    def __init__(self):
        self.user = User()
        pass

    def load_user(self, user_id):
        return User.objects(pk=user_id).first()

    def register(self):
        form = RegForm()
        if request.method == 'POST':

            if form.validate():
                existing_user = User.objects(email=form.email.data).first()
                if existing_user is None:
                    hashpass = generate_password_hash(form.password.data, method='sha256')
                    # return form.email+'   '+hashpass
                    hey = User(form.email.data, hashpass).save()
                    login_user(hey)
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('register.html', form=form,
                                           server_errors=['Your email is already registered!'])
        return render_template('register.html', form=form)

    def login(self):
        if current_user.is_authenticated == True:
            return redirect(url_for('dashboard'))
        form = RegForm()
        if request.method == 'POST':
            if form.validate():
                check_user = User.objects(email=form.email.data).first()
                if check_user:
                    if check_password_hash(check_user['password'], form.password.data):
                        login_user(check_user)
                        return redirect(url_for('dashboard'))
                    else:
                        return render_template('login.html', form=form, server_errors=['Wrong email or password!'])
                else:
                    return render_template('login.html', form=form, server_errors=['Wrong email or password!'])
            else:
                return render_template('login.html', form=form, server_errors=['Wrong email or password!'])
        return render_template('login.html', form=form)

    def logout(self):
        logout_user()
        return redirect(url_for('login'))

    def route(self):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))