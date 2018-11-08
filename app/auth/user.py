from flask_login import UserMixin

from .__init__ import db


class User(UserMixin, db.Document):

    meta = {'collection': 'users'}
    email = db.StringField()
    password = db.StringField()

    def __repr__(self):
        return 'emaily: '+self.email+', password: '+self.password

    def __str__(self):
        return 'my str'

