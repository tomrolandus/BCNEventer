import mongoengine, pandas as pd
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datasets.MeetUp.categories import categories
from datasets.Xceed.genres import music_genres
import numpy as np
from .base import Base


class User(Base, UserMixin):
    __min_password_length = 8
    __max_password_length = 20

    email = mongoengine.EmailField(required=True)
    password = mongoengine.StringField()

    RATES = 'Rates'
    MOVIES = 'Events'

    ratings = pd.DataFrame({MOVIES: [], RATES: []})
    preferences_keys = mongoengine.ListField()
    music_genres_keys = mongoengine.ListField()
    age = mongoengine.IntField()
    gender = mongoengine.IntField()





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

        return 'email: '+self.email + "<br>Preference keys: " +  prefs + "<br>Music genres keys: " +\
               genres + "<br>Gender: " + str(self.gender) + "<br>Age: " + str(self.age) + "<br><br>"
        #+', password: '+self.password

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

    def set_preferences_keys(self, prefs):
        self.preferences_keys = prefs
        self.save()

    def get_preferences_keys(self):
        return self.preferences_keys

    def get_preferences_names(self):
        return [categories[i] for i in self.preferences_keys]


    def get_age(self):
        return self.age

    def set_age(self,age):
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


    def _create_music_persona(self, persona_nb=0):
        if persona_nb == 0:
            persona_nb = np.random.randint(1, 5)
        if persona_nb == 1:
            self.music_genres_keys = [1, 2, 3, 4, 5, 6, 7]
            # self.music_genres = ['techno','tech house','deep house','house',
            # 'minimal','electronic', 'electro']

        if persona_nb == 2:
            self.music_genres_keys = [8, 11, 12, 17, 18]
            # self.music_genres = ['dance','r&b','reggae dancehall','latin',
            # 'reggaeton']

        if persona_nb == 3:
            self.music_genres_keys = [8, 9, 13, 15, 16, 19]

            # self.music_genres = ['dance', 'funky', 'hits', 'pop', 'indie rock',
            #                      'nu disco']

        if persona_nb == 4:
            self.music_genres_keys = [3, 10, 11, 14, 7]
            # self.music_genres = ['deep house','hip hop','r&b', 'urban','electro']


    def _randomly_modify_music_genres(self, nb_to_add=2, nb_to_remove=2):
        not_selected_genres = list(set(music_genres) ^ set(self.music_genres_keys))

        if nb_to_remove > len(self.music_genres_keys):
            nb_to_remove = len(self.music_genres_keys)

        if nb_to_add > len(not_selected_genres):
            nb_to_add = len(not_selected_genres)

        for i in range(0, nb_to_remove):
            self.music_genres_keys.pop(np.random.randint(0, len(self.music_genres_keys) - i))

        for j in range(0, nb_to_add):
            to_add = np.random.randint(1, len(not_selected_genres) - j)
            self.music_genres_keys.append(not_selected_genres[to_add])
            not_selected_genres.pop(to_add)

    def create_semi_random_persona(self):
        self._create_music_persona()
        self._create_preferences_persona()
        self._randomly_modify_preferences()
        self._randomly_modify_music_genres()
        self.set_age(np.random.randint(14,75))
        self.set_gender(np.random.randint(0,3))

        self.save()

    def create_user_deprecated(user_name, events):
        np.random.seed(500)
        user = User(user_name)
        for event in events:
            user.rate(event, np.random.uniform(0, 5))
        return user

    def _randomly_modify_preferences(self, nb_to_add=2, nb_to_remove=2):
        not_selected_preferences = list(set(self.preferences_keys) ^ set(categories))

        if nb_to_remove > len(self.preferences_keys):
            nb_to_remove = len(self.preferences_keys)

        if nb_to_add > len(not_selected_preferences):
            nb_to_add = len(not_selected_preferences)

        for i in range(0, nb_to_remove):
            self.preferences_keys.pop(np.random.randint(0, len(self.preferences_keys) - i))

        for j in range(0, nb_to_add):
            to_add = np.random.randint(1, len(not_selected_preferences) - j)
            self.preferences_keys.append(not_selected_preferences[to_add])
            not_selected_preferences.pop(to_add)

    def _create_preferences_persona(self, preference_type=0):
        if preference_type == 0:
            preference_type = np.random.randint(1, 6)
        if preference_type == 1:  # bookworm
            self.preferences_keys = [1, 18, 6, 20, 27, 35]
            # self.preferences = ["Arts & Culture","Book Clubs","Education & Learning",
            #                   "Movies & Film","Photography","Writing"]

        if preference_type == 2:  # career driven
            self.preferences_keys = [2, 6, 14, 31, 34, 32]
            # self.preferences = ["Career & Business","Education & Learning","Fitness",
            #                    "Health & Wellbeing","Socializing","Tech","Sports & Recreation"]
        if preference_type == 3:  # outdoorsy
            self.preferences_keys = [3, 9, 15, 21, 23, 26, 32]
            # self.preferences = ["Cars & Motorcycles","Fitness","Hobbies & Crafts","Music",
            #                    "Outdoors & Adventure","Pets & Animals","Sports & Recreation"]

        if preference_type == 4:  # alternative
            self.preferences_keys = [1, 4, 8, 10, 15, 16, 12, 20, 21, 22, 26, 27, 28]
            # self.preferences = ["Arts & Culture","Community & Environment","Fashion & Beauty",
            #                     "Food & Drink","Hobbies & Crafts", "Language & Ethnic Identity",
            #                     "LGBT", "Movies & Film", "Music", "New Age & Spirituality",
            #                     "Pets & Animals","Photography","Religion & Beliefs",]

        if preference_type == 5:  # social
            self.preferences_keys = [5, 20, 4, 10, 11, 21, 25, 31, 33]
            # self.preferences = ["Dancing","Movies & Film","Community & Environment","Food & Drink",
            #                      "Games","Music","Parents & Family","Socializing","Support"]



