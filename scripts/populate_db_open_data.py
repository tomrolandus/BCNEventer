

## Modules
import pymongo
import pandas as pd
import library as lib

## Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
    print ("Could not connect to MongoDB: %s" % e) 

## Set up database and collection
db = conn['events']
collection = db.opendata

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

## Street Markets
street_markets = lib.load_and_prepare_data(cnames, lib.rename_cols_street_markets, "../datasets/OpenDataBCN/street_markets.csv")
lib.write_db(street_markets, "Street Markets", collection)

## Cultural activities
cultural_activities = lib.load_and_prepare_data(cnames, lib.rename_cols_cultural_activities, "../datasets/OpenDataBCN/cultural_activities.csv")
lib.write_db(cultural_activities, "Cultural Activities", collection)

## Temporary expos
temporary_expos = lib.load_and_prepare_data(cnames, lib.rename_cols_temporary_expos, "../datasets/OpenDataBCN/temporary_expos.csv")
lib.write_db(temporary_expos, "Temporary Expos", collection)