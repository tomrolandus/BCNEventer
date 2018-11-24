
# TODO: fix geocoding
# TODO: convert categories to ids
# TODO: loop oer rows of dataframe in write_db and write each row to the db


#%% Modules
import sys
sys.path.append('./app/')
sys.path.append('./scripts/')

import pymongo
import library as lib
import pandas as pd

#from models.event import Event

#%% Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
    print ("Could not connect to MongoDB: %s" % e) 

"""name='', description='', location=(0, 0), date_time=0, category_ids=None"""

cnames = [
    'name', # 0
    'description', #1
    'location', #2
    'date_time', #3
    'category_ids' #4
]

## Set up database and collection
db = conn['bcneventer']

## Meetup
col_meetup = db.meetup
meetup = lib.load_and_prepare_data(cnames, lib.rename_cols_meetup, "../datasets/MeetUp/events_Barcelona.csv", delimiter_ = ";")
lib.write_db(meetup, "Meetup", col_meetup)
