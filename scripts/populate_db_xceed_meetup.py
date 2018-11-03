
## Modules
import pymongo
import library as lib
import pandas as pd


## Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
    print ("Could not connect to MongoDB: %s" % e) 

## Set up database and collection
db = conn['events']
collection = db.exceed

cnames = ['lat', #0
          'long', #1
          'event_type', #2
          'address', #3 
          'start_date', #4
          'end_date', #5
          'event_info', #6
          'web', #7
          'image', #8
          'tickets', #9
          'year', #10
          'location', #11
          'event_name', #12
          'price', #13
         ] 

## Xceed
xceed = lib.load_and_prepare_data(cnames, lib.rename_cols_exceed, "../datasets/Xceed/xceed_barcelona.csv")
lib.write_db(xceed, "Xceed", collection)

## Meetup
collection = db.meetup