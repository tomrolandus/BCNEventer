
#%%
import sys
sys.path.append('../')

from flask import Flask
from flask_mongoengine import MongoEngine
from app.models.user import User

from faker import Faker

app = Flask(__name__)
app.config['MONGODB_DB'] = 'bcneventer'
app.config['MONGODB_HOST'] = "mongodb://localhost:27017/bcneventer"

db = MongoEngine(app)

faker = Faker()

#%%
User.drop_collection()

n = 10

# Test user
user = User.create('test@test.com', '12345678')

for i in range(n):
    user = User.create(faker.safe_email(), faker.password())
