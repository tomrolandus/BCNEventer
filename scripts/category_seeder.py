from faker import Faker
from flask import Flask
from flask_mongoengine import MongoEngine

from app.models.category import Category

app = Flask(__name__)
app.config['MONGODB_DB'] = 'bcneventer'
app.config['MONGODB_HOST'] = "mongodb://localhost:27017/bcneventer"

db = MongoEngine(app)

faker = Faker()

cats = [
    'Arts & Culture',
    'Book Clubs',
    'Career & Business',
    'Cars & Motorcycles',
    'Community & Environment',
    'Dancing',
    'Education & Learning',
    'Fashion & Beauty',
    'Fitness',
    'Food & Drink',
    'Games',
    'Health & Wellbeing',
    'Hobbies & Crafts',
    'Language & Ethnic Identity',
    'LGBT',
    'Movies & Film',
    'Music',
    'New Age & Spirituality',
    'Outdoors & Adventure',
    'Parents & Family',
    'Pets & Animals',
    'Photography',
    'Religion & Beliefs',
    'Singles',
    'Socializing',
    'Sports & Recreation',
    'Support',
    'Tech',
    'Writing'
]

for cat in cats:
    Category(cat).save()
