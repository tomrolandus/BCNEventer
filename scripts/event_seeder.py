import sys
sys.path.append('../')

from flask import Flask
from flask_mongoengine import MongoEngine

from app.models.category import Category
from app.models.event import Event

from faker import Faker

app = Flask(__name__)
app.config['MONGODB_DB'] = 'bcneventer'
app.config['MONGODB_HOST'] = "mongodb://localhost:27017/bcneventer"

db = MongoEngine(app)

faker = Faker()

categories = Category.objects
Event.drop_collection()

n = 1000


for i in range(n):
    random_geo = [faker.random.uniform(41.374761, 41.424576),
                  faker.random.uniform(2.121801, 2.191643)]  # location in BCN

    random_cats = faker.random.sample(list(categories), round(0.5 + faker.random.betavariate(2, 5) * 3))

    event = Event(faker.sentence(nb_words=4), faker.text(), random_geo,
                  faker.date_time_this_year(after_now=True), random_cats).save()
