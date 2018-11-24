
#%% Modules
import pymongo
import pandas as pd
from geopy.geocoders import Nominatim

import sys
sys.path.append('./app/')
sys.path.append('./scripts/')

#from models.event import Event

#%% Helpers
''' cnames_philippe = [
    'name', # 0
    'description', #1
    'location', #2
    'date_time', #3
    'category_ids' #4
] '''

''' cnames = ['lat', #0
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
              'category', #14
         ]  '''
def drop_columns(data, cnames):
    drop_columns = list(set(data.columns) - set(cnames))
    data = data.drop(drop_columns, axis = 1)
    return(data)
def load_and_prepare_data(cnames, rename_cols_fct, path, delimiter_ = None):
    if delimiter_ is None: data = pd.read_csv(path)
    else: data = pd.read_csv(path, delimiter=delimiter_)
    location = list(zip(data.coordinates0, data.coordinates2))
    data["location"] = location
    data = rename_cols_fct(cnames, data)
    data = drop_columns(data, cnames)
    return(data)
def rename_cols_meetup(cnames, data):
    data = data.rename(columns={'Event':cnames[0],
                                'location': cnames[2],
                                'Time': cnames[3],
                                'category':cnames[4]
                                })
    data.date_time = pd.to_datetime(data.date_time, unit='ms').astype(str)
    # add a column for address, as given by reverse geocoding the coordinates
    # data[cnames[1]] = data.apply(lambda row: getAddress(row['location'][0],row['location'][1]),axis=1)
    return(data)
def write_db(data, data_name, collection):
    try:

        collection.insert_many(data.to_dict("records"))
        print("%s data successfully written to DB!!!" % data_name)
    except pymongo.errors.WriteError as e:
        print("Could not write %s data to DB: %s" % (data_name, e))

geolocator = Nominatim(user_agent="bcneventer")
def getAddress(lat, long):
    try:
        address = geolocator.reverse("" + lat + ", " + long + "").address
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

