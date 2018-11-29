import sys

sys.path.append('../')

from app.models.user import User
from flask import Flask
from flask_mongoengine import MongoEngine
import mongoengine

from faker import Faker

from app.models.event import Event
from app.models.event import Category

from datasets.MeetUp.categories import categories
from datasets.Xceed.genres import music_genres

import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['MONGODB_DB'] = 'bcneventer'
app.config['MONGODB_HOST'] = "mongodb://localhost:27017/bcneventer"

db = MongoEngine(app)

faker = Faker()

game = Category.objects(name="Music")

games_events = Event.objects(categories=game)
for event in games_events:
    print(event.name)







def create_music_persona(user, persona_nb=0):
    if persona_nb == 0:
        persona_nb = np.random.randint(1, 5)
    if persona_nb == 1:
        music_genres_keys = [1, 2, 3, 4, 5, 6, 7]
        # music_genres = ['techno','tech house','deep house','house',
        # 'minimal','electronic', 'electro']

    if persona_nb == 2:
        music_genres_keys = [8, 11, 12, 17, 18]
        # music_genres = ['dance','r&b','reggae dancehall','latin',
        # 'reggaeton']

    if persona_nb == 3:
        music_genres_keys = [8, 9, 13, 15, 16, 19]

        # music_genres = ['dance', 'funky', 'hits', 'pop', 'indie rock',
        #                      'nu disco']

    if persona_nb == 4:
        music_genres_keys = [3, 10, 11, 14, 7]
        # music_genres = ['deep house','hip hop','r&b', 'urban','electro']


def randomly_modify_music_genres(user, nb_to_add=2, nb_to_remove=2):
    music_genres_keys = user.get_music_genres_keys()
    not_selected_genres = list(set(music_genres) ^ set(music_genres_keys))

    if nb_to_remove > len(music_genres_keys):
        nb_to_remove = len(music_genres_keys)

    if nb_to_add > len(not_selected_genres):
        nb_to_add = len(not_selected_genres)

    for i in range(0, nb_to_remove):
        music_genres_keys.pop(np.random.randint(0, len(music_genres_keys) - i))

    for j in range(0, nb_to_add):
        to_add = np.random.randint(1, len(not_selected_genres) - j)
        music_genres_keys.append(not_selected_genres[to_add])
        not_selected_genres.pop(to_add)


def randomly_modify_preferences(user, nb_to_add=2, nb_to_remove=2):
    preferences_keys = user.get_preferences_keys()
    not_selected_preferences = list(set(user.preferences_keys) ^ set(categories))

    if nb_to_remove > len(preferences_keys):
        nb_to_remove = len(preferences_keys)

    if nb_to_add > len(not_selected_preferences):
        nb_to_add = len(not_selected_preferences)

    for i in range(0, nb_to_remove):
        preferences_keys.pop(np.random.randint(0, len(preferences_keys) - i))

    for j in range(0, nb_to_add):
        to_add = np.random.randint(1, len(not_selected_preferences) - j)
        preferences_keys.append(not_selected_preferences[to_add])
        not_selected_preferences.pop(to_add)


def create_preferences_persona(user, preference_type=0):
    categories_ids = [] # mongoengine.ListField(mongoengine.ReferenceField(Category))
    test = mongoengine.ListField(mongoengine.ReferenceField(Category))
    if preference_type == 0:
        preference_type = np.random.randint(1, 6)
    if preference_type == 1:  # bookworm
        #preferences_keys = [1, 18, 6, 20, 27, 35]
        preferences = ["Arts & Culture","Book Clubs","Education & Learning",
                          "Movies & Film","Photography","Writing"]
        for pref in preferences:
            categories_ids.append(Category.objects(name = pref)[0])

    if preference_type == 2:  # career driven
        #preferences_keys = [2, 6, 14, 31, 34, 32]
        preferences = ["Career & Business","Education & Learning","Fitness",
                           "Health & Wellbeing","Socializing","Tech","Sports & Recreation"]
        for pref in preferences:
            categories_ids.append(Category.objects(name = pref)[0])
    if preference_type == 3:  # outdoorsy
        # preferences_keys = [3, 9, 15, 21, 23, 26, 32]
        preferences = ["Cars & Motorcycles","Fitness","Hobbies & Crafts","Music",
                           "Outdoors & Adventure","Pets & Animals","Sports & Recreation"]
        for pref in preferences:
            categories_ids.append(Category.objects(name = pref)[0])

    if preference_type == 4:  # alternative
        # preferences_keys = [1, 4, 8, 10, 15, 16, 12, 20, 21, 22, 26, 27, 28]
        preferences = ["Arts & Culture","Community & Environment","Fashion & Beauty",
                            "Food & Drink","Hobbies & Crafts", "Language & Ethnic Identity",
                            "LGBT", "Movies & Film", "Music", "New Age & Spirituality",
                            "Pets & Animals","Photography","Religion & Beliefs",]
        for pref in preferences:
            categories_ids.append(Category.objects(name = pref)[0])

    if preference_type == 5:  # social
        # preferences_keys = [5, 20, 4, 10, 11, 21, 25, 31, 33]
        preferences = ["Dancing","Movies & Film","Community & Environment","Food & Drink",
                             "Games","Music","Parents & Family","Socializing","Support"]
        for pref in preferences:
            categories_ids.append(Category.objects(name = pref)[0])






def create_semi_random_persona(user):
    #create_music_persona()
    create_preferences_persona(user)
    #randomly_modify_preferences()
    #randomly_modify_music_genres()
    #user.set_age(np.random.randint(14, 75))
    #user.set_gender(np.random.randint(0, 3))

def create_users(n=20):
    for i in range(1, n):
        email = faker.safe_email()  # 'user' + str(i) + '@test.com'
        password = '12345678'
        user = User.create(email, password)
        create_semi_random_persona(user)

    return


create_users()