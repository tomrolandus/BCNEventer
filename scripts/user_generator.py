import sys

from mongoengine import ListField

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


def randomly_modify_preferences(user):
    user.save()
    user_categories = user.get_categories()
    not_selected_categories = list(set(user_categories) ^ set(Category.objects()))
    categories_to_add = faker.random.sample(list(not_selected_categories), round(0.5 + faker.random.betavariate(2, 5) * 3))
    categories_to_remove = faker.random.sample(list(user_categories), round(0.5 + faker.random.betavariate(2, 5) * 3))
    user.add_categories(categories_to_add)
    user.reload()
    user.remove_categories(categories_to_remove)
    user.reload()


def create_preferences_persona(user, preference_type=0):
    if preference_type == 0:
        preference_type = np.random.randint(1, 6)
    if preference_type == 1:  # bookworm
        #preferences_keys = [1, 18, 6, 20, 27, 35]
        preferences = ["Arts & Culture","Book Clubs","Education & Learning",
                          "Movies & Film","Photography","Writing"]


    if preference_type == 2:  # career driven
        #preferences_keys = [2, 6, 14, 31, 34, 32]
        preferences = ["Career & Business","Education & Learning","Fitness",
                           "Health & Wellbeing","Socializing","Tech","Sports & Recreation"]

    if preference_type == 3:  # outdoorsy
        # preferences_keys = [3, 9, 15, 21, 23, 26, 32]
        preferences = ["Cars & Motorcycles","Fitness","Hobbies & Crafts","Music",
                           "Outdoors & Adventure","Pets & Animals","Sports & Recreation"]



    if preference_type == 4:  # alternative
        # preferences_keys = [1, 4, 8, 10, 15, 16, 12, 20, 21, 22, 26, 27, 28]
        preferences = ["Arts & Culture","Community & Environment","Fashion & Beauty",
                            "Food & Drink","Hobbies & Crafts", "Language & Ethnic Identity",
                            "LGBT", "Movies & Film", "Music", "New Age & Spirituality",
                            "Pets & Animals","Photography","Religion & Beliefs",]


    if preference_type == 5:  # social
        # preferences_keys = [5, 20, 4, 10, 11, 21, 25, 31, 33]
        preferences = ["Dancing","Movies & Film","Community & Environment","Food & Drink",
                             "Games","Music","Parents & Family","Socializing","Support"]

    cats = []
    for pref in preferences:
        cats.append(Category.objects(name = pref)[0])

    user.set_categories(cats)

def create_semi_random_persona(user):
    #create_music_persona()
    create_preferences_persona(user)
    randomly_modify_preferences(user)
    #randomly_modify_music_genres()
    #user.set_age(np.random.randint(14, 75))
    #user.set_gender(np.random.randint(0, 3))



def link_random_events_to_user(user):
    events_from_categories = Event.objects(categories__in = user.get_categories())
    random_events = faker.random.sample(list(events_from_categories), round(0.5 + faker.random.betavariate(2, 5) * 10))
    user.set_events(random_events)

def create_users(n=1):
    User.drop_collection()
    for i in range(0, n):
        email = faker.safe_email()  # 'user' + str(i) + '@test.com'
        password = '12345678'
        user = User.create(email, password)
        create_semi_random_persona(user)
        link_random_events_to_user(user)



    return


create_users()