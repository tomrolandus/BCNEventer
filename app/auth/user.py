from .__init__ import db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


class User(UserMixin, db.Document):

    meta = {'collection': 'users'}
    email = db.StringField()
    password = db.StringField()

    def __repr__(self):
        return 'emaily: '+self.email+', password: '+self.password

    def __str__(self):
        return 'my str'

