
#%%

## Modules
import pymongo
import library as lib
import pandas as pd

try:
    # use your database name, user and password here:
    # mongodb://<dbuser>:<dbpassword>@<mlab_url>.mlab.com:57066/<database_name>
    with open("../credentials.txt", 'r', encoding='utf-8') as f:
        [name, password, url, dbname] = f.read().splitlines()
    conn = pymongo.MongoClient("mongodb://{}:{}@{}/{}".format(name, password, url, dbname))
    print("Connected successfully!!!")

except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB: %s" % e)
conn

cnames = [
    'name', # 0
    'description', #1
    'location', #2
    'date_time', #3
    'category_ids' #4
]


## Set up database and collection
db = conn['bcneventer']

## Xceed
#col_xceed = db.exceed
#xceed = lib.load_and_prepare_data(cnames, lib.rename_cols_exceed, "../datasets/Xceed/xceed_barcelona.csv")
#lib.write_db(xceed, "Xceed", col_xceed)


## Meetup
col_meetup = db.meetup
meetup = lib.load_and_prepare_data(cnames, lib.rename_cols_meetup, "../datasets/MeetUp/events_Barcelona.csv", delimiter_ = ";")
lib.write_db(meetup, "Meetup", col_meetup)
