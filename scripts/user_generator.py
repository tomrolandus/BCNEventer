from app.models.user import User
from flask import Flask
from flask_mongoengine import MongoEngine

from datasets.MeetUp.categories import categories
from datasets.Xceed.genres import music_genres


import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['MONGODB_DB'] = 'bcneventer'
app.config['MONGODB_HOST'] = "mongodb://localhost:27017/bcneventer"

db = MongoEngine(app)


def create_users(n= 20, csv = True):
    users_list = []
    labels = ['email','password','preference_keys', 'music_genres_keys','gender','age']
    for i in range(1,n):
        email = 'user' + str(i) + '@test.com'
        password = '12345678'
        user = User.create(email, password)#, preferences_keys, music_genres_keys)
        User.create_semi_random_persona(user)

        preferences_keys = User.get_preferences_keys(user)
        music_genres_keys = User.get_music_genres_keys(user)

        age = User.get_age(user)
        gender = User.get_gender(user)
        print(gender)
        users_list.append([email,password,preferences_keys, music_genres_keys, gender,age])

    if csv:
        df = pd.DataFrame.from_records(users_list, columns=labels)
        df.to_csv("users_list.csv")

    return 'done!'


create_users()