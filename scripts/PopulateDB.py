

## Modules
import pymongo
import pandas as pd

## Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
    print ("Could not connect to MongoDB: %s" % e) 

## Set up database and collection
db = conn['events']
collection = db.opendata

## column names definitions
cnames = ['lat', #0
          'long', #1
          'event_type', #2
          'address', #3 
          'start_date', #4
          'end_date', #5
          'event_info', #6
          'web', #7
          'image', #8
          'tickets' #9
         ] 

## Helpers
def drop_columns(data):
    drop_columns = list(set(data.columns) - set(cnames))
    data = data.drop(drop_columns, axis = 1)
    return(data)
def rename_cols_street_markets(cnames, data):
    data = data.rename(columns={'NOM_CAPA':cnames[2], 'LONGITUD':cnames[1], 'LATITUD': cnames[0],
                                   'ADRECA': cnames[3] })
    data[cnames[2]] = 'Street Markets'
    return(data)
def load_and_prepare_data(cnames, rename_cols_fct, path):
    data = pd.read_csv(path)
    data = rename_cols_fct(cnames, data)
    data = drop_columns(data)
    return(data)
def rename_cols_street_markets(cnames, data):
    data.rename(columns={'NOM_CAPA':cnames[2], 'LONGITUD':cnames[1], 'LATITUD': cnames[0],
                                   'ADRECA': cnames[3] }, inplace = True)
    data[cnames[2]] = 'Street Markets'
    return(data)
def rename_cols_cultural_activities(cnames, data):
    data = data.rename(columns={'Data fi':cnames[5], 'Data inici':cnames[4], 'Descripció': cnames[6],
                                   'Enllaços': cnames[7], 'Imatges': cnames[8], 'Entrades': cnames[9]})
    return(data)
def write_db(data, data_name):
    try:
        collection.insert_many(data.to_dict("records"))
        print("%s data successfully written to DB!!!" % data_name)
    except pymongo.errors.WriteError as e:
        print("Could not write %s data to DB: %s" % (data_name, e))


## Street Markets
street_markets = load_and_prepare_data(cnames, rename_cols_street_markets, "../datasets/OpenDataBCN/street_markets.csv")
write_db(street_markets, "Street Markets")

## Cultural activities
cultural_activities = load_and_prepare_data(cnames, rename_cols_cultural_activities, "../datasets/OpenDataBCN/cultural_activities.csv")
write_db(cultural_activities, "Cultural Activities")