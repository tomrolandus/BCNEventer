import mongoengine
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base


class User(Base, UserMixin):
    __min_password_length = 8
    __max_password_length = 20

    email = mongoengine.EmailField(required=True)
    password = mongoengine.StringField()

    @staticmethod
    def create(email, password):
        if len(password) < User.__min_password_length or len(password) > User.__max_password_length:
            raise Exception('password_length')

        hashedpwd = generate_password_hash(password, method='sha256')
        return User(email=email, password=hashedpwd).save()

    def login(self, password):
        self.reload()
        if not self.id:
            return None

        if check_password_hash(self.password, password):
            return self

        return None
