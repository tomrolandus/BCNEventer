
## Modules
import pymongo
import pandas as pd
from geopy.geocoders import Nominatim

## Helpers
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
    data = rename_cols_fct(cnames, data)
    data = drop_columns(data, cnames)
    return(data)
def rename_cols_street_markets(cnames, data):
    data.rename(columns={'NOM_CAPA':cnames[2], 'LONGITUD':cnames[1], 'LATITUD': cnames[0],
                                   'ADRECA': cnames[3] })
    data[cnames[2]] = 'Street Markets'
    return(data)
def rename_cols_cultural_activities(cnames, data):
    data = data.rename(columns={'Data fi':cnames[5], 'Data inici':cnames[4], 'Descripció': cnames[6],
                                   'Enllaços': cnames[7], 'Imatges': cnames[8], 'Entrades': cnames[9]})
    return(data)
def rename_cols_temporary_expos(cnames, data):
    data = data.rename(columns={'Any':cnames[10], 'Latitud':cnames[0], 'Longitud': cnames[1],
                                   'Web': cnames[7], 'Seu': cnames[11]})
    # add a column for address, as given by reverse geocoding the coordinates
    data[cnames[3]] = data.apply(lambda row: getAddress(row['lat'], row['long']), axis=1)
    return(data)
def rename_cols_exceed(cnames, data):
    data = data.rename(columns={'description':cnames[12], 'start time':cnames[4], 'place': cnames[11],
                                'musice style': cnames[6], 'price': cnames[13]})
    # add columns for coordinates, as given by geocoding the location
    data[cnames[0]], data[cnames[1]] = zip(*data[cnames[11]].map(getCoordinates))
    return(data)
def rename_cols_meetup(cnames, data):
    data = data.rename(columns={'coordinates0':cnames[0], 'coordinates2':cnames[1], 'Time': cnames[4],
                                'Event': cnames[12]})
    data.start_date = pd.to_datetime(data.start_date, unit='ms').astype(str)
    # add a column for address, as given by reverse geocoding the coordinates
    data[cnames[3]] = data.apply(lambda row: getAddress(row['lat'],row['long']),axis=1)
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

