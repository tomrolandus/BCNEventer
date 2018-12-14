import mongoengine
import numpy as np
import pandas as pd
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.category import Category
# from datasets.MeetUp.categories import categories
from datasets.Xceed.genres import music_genres
from .base import Base
from app.models.event import Event


class User(Base, UserMixin):
    __min_password_length = 8
    __max_password_length = 20

    email = mongoengine.EmailField(required=True)
    password = mongoengine.StringField()

    RATES = 'Rates'
    MOVIES = 'Events'

    ratings = pd.DataFrame({MOVIES: [], RATES: []})
    categories = mongoengine.ListField(mongoengine.ReferenceField(Category))
    events = mongoengine.ListField(mongoengine.ReferenceField(Event))
    music_genres_keys = mongoengine.ListField()
    age = mongoengine.IntField()
    gender = mongoengine.IntField()
    name = mongoengine.StringField()

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

    def __repr__(self):
        prefs = ""
        for pref in self.preferences_keys:
            prefs += "-" + str(pref)
        genres = ""
        for genre in self.music_genres_keys:
            genres += '-' + str(genre)

        return 'email: ' + self.email + "<br>Preference keys: " + prefs + "<br>Music genres keys: " + \
               genres + "<br>Gender: " + str(self.gender) + "<br>Age: " + str(self.age) + "<br><br>"
        # +', password: '+self.password


    def rate(self, movie, rating):
        try:
            if movie in self.ratings[self.MOVIES].tolist():
                self.ratings.loc[self.ratings[self.MOVIES] == movie, self.self.RATES] = rating
            else:
                self.ratings.append(pd.Series({self.MOVIES: movie, self.RATES: rating}))
        except TypeError:
            self.ratings = self.ratings.append(pd.Series({self.MOVIES: movie, self.RATES: rating}), ignore_index=True)

    def retrieve_rate(self, movie):
        return self.ratings.loc[self.ratings[self.MOVIES] == movie][self.RATES]

    def retrieve_movies_between(self, minrate, maxrate):
        return self.ratings[(self.ratings[self.RATES] < maxrate) & (self.ratings[self.RATES] > minrate)]

    def retrieve_df(self):
        return self.ratings

    def get_email(self):
        return self.email

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age
        self.save()

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender
        self.save()

    def set_music_genres(self, genres):
        self.music_genres = genres
        self.save()

    def get_music_genres_keys(self):
        return self.music_genres_keys

    def get_music_genres_names(self):
        return [music_genres[i] for i in self.music_genres_keys]

    def set_categories(self, categories):
        self.categories = categories
        self.save()

    def add_categories(self, categories_to_add):
        self.update(push_all__categories=categories_to_add)
        self.save()

    def remove_categories(self, categories_to_remove):
        self.update(pull_all__categories=categories_to_remove)
        self.save()

    def get_categories(self):
        return self.categories

    def set_events(self, events):
        self.events = events
        self.save()

    def add_events(self, events_to_add):
        self.update(push_all__events = events_to_add)
        self.save()

    def get_events(self):
        return self.events

    def set_name(self, name):
        self.name = name
        self.save()

    def get_name(self):
        return self.name

