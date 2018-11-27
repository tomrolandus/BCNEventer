import sys
sys.path.append('../')

from app.models.user import User
from flask import Flask
from flask_mongoengine import MongoEngine

from faker import Faker

from app.models.event import Event

from datasets.MeetUp.categories import categories
from datasets.Xceed.genres import music_genres


import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['MONGODB_DB'] = 'bcneventer'
app.config['MONGODB_HOST'] = "mongodb://localhost:27017/bcneventer"

db = MongoEngine(app)

faker = Faker()

events = Event.objects[0]
print(events)

def create_users(n= 20):
    users_list = []
    labels = ['email','password','preference_keys', 'music_genres_keys','gender','age']
    for i in range(1,n):
        email = faker.safe_email() #'user' + str(i) + '@test.com'
        password = '12345678'
        user = User.create(email, password)#, preferences_keys, music_genres_keys)
        User.create_semi_random_persona(user)

    return


create_users()