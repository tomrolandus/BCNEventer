import mongoengine
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.category import Category
from app.models.event import Event
from datasets.Xceed.genres import music_genres
from .base import Base


class User(Base, UserMixin):
    __min_password_length = 8
    __max_password_length = 20

    email = mongoengine.EmailField(required=True)
    password = mongoengine.StringField()

    categories = mongoengine.ListField(mongoengine.ReferenceField(Category))
    events = mongoengine.ListField(mongoengine.ReferenceField(Event))
    name = mongoengine.StringField()
    recommended_events = mongoengine.ListField(mongoengine.ReferenceField(Event))
    music_genres_keys = mongoengine.ListField()

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
        self.update(push_all__events=events_to_add)
        self.save()

    def get_events(self):
        return self.events

    def set_recommended_events(self, recommended_events):
        self.update(pull_all__recommended_events=self.recommended_events)
        self.update(push_all__recommended_events=recommended_events)


    def set_name(self, name):
        self.name = name
        self.save()

    def get_name(self):
        return self.name