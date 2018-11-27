
#%% Modules
import pymongo
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


import sys
sys.path.append('../')
sys.path.append('./scripts/')

from datetime import datetime

from app.models.event import Event
from app.models.category import Category

#%% Helpers
def connect_to_prod_db():
    try:
        # use your database name, user and password here:
        # mongodb://<dbuser>:<dbpassword>@<mlab_url>.mlab.com:57066/<database_name>
        with open("../credentials.txt", 'r', encoding='utf-8') as f:
            [name, password, url, dbname] = f.read().splitlines()
        conn = pymongo.MongoClient("mongodb://{}:{}@{}/{}".format(name, password, url, dbname))
        print("Writing data to production db...")
        return conn

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)

def connect_to_local_db():
    # %% Connection to Mongo DB
    try:
        conn = pymongo.MongoClient()
        print("Writing data to local db...")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)

def query_category_ids(cat_ids_from_prod):
    """
    Queries production db and returns
    :return: dict
        with key = category_name
        with value = category_id
    """
    if cat_ids_from_prod:
        db_conn = connect_to_prod_db()
    else:
        db_conn = connect_to_local_db()
    db_prod = db_conn['bcneventer'].category.find()
    cat_to_id = {}
    for elem in db_prod:
        cat_to_id[elem['name']] = elem['_id']

    return cat_to_id

def convert_category_to_id(data, cat_ids_from_prod):
    cat_to_id = query_category_ids(cat_ids_from_prod)
    data.category_ids = [cat_to_id[cat] for cat in data.category_ids]
    return data

def drop_columns(data, cnames):
    drop_columns = list(set(data.columns) - set(cnames))
    data = data.drop(drop_columns, axis = 1)
    return(data)

def load_and_prepare_data(cnames, rename_cols_fct, path, cat_ids_from_prod, delimiter_ = None):
    if delimiter_ is None: data = pd.read_csv(path)
    else: data = pd.read_csv(path, delimiter=delimiter_)
    data.dropna(inplace = True)
    data = rename_cols_fct(cnames, data)
    data = drop_columns(data, cnames)
    data = convert_category_to_id(data, cat_ids_from_prod)
    return(data)

def rename_cols_meetup(cnames, data):
    location = []
    for (loc1, loc2) in zip(data.coordinates0, data.coordinates2):
        try:
            location.append((float(loc1), float(loc2)))
        except:
            location.append((0,0))

    data["location"] = location
    data = data.rename(columns={'Event':cnames[0],
                                'location': cnames[2],
                                'Time': cnames[3],
                                'category':cnames[4]
                                })
    data.date_time = pd.to_datetime(data.date_time, unit='ms').astype(str)
    # add the address as the description column, as given by reverse geocoding the coordinates
    data[cnames[1]]  = [getAddress(str(location[0]),str(location[1])) for location in data.location]
    return(data)

def rename_cols_exceed(cnames, data):
    data = data.rename(columns={'description':cnames[0], # map description from csv to cnames[0] = name in output
                                'start time':cnames[3]
                                })
    # add columns for coordinates, as given by geocoding the location
    data['lat'], data['long'] = zip(*data['place'].map(getCoordinates))
    return(data)

def write_df_to_db(data):
    for i in range(data.shape[0]):
        event = Event(data.iloc[i]['name'],
                      data.iloc[i]['description'],
                      data.iloc[i]['location'],
                      data.iloc[i]['date_time'],
                      [data.iloc[i]['category_ids']]).save()
    print("Events successfully written to db!")

geolocator = Nominatim(user_agent="bcneventer")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def getAddress(lat, long):
    try:
        if lat == 'None' or long == 'None':
            return ""
        address = geolocator.reverse("" + lat + ", " + long + "").address
        if address == None:
            return ""
        else:
            return address.split(', Barcelona')[0]
    except:
        return ""

def getCoordinates(location):
    try:
        if 'Barcelona' not in location:
            location = location + ' Barcelona'
        coordinates = geolocator.geocode(location)
        return coordinates.latitude, coordinates.longitude
    except:
        return 0,0

