
## Modules
import pymongo
import pandas as pd

## Helpers
def drop_columns(data, cnames):
    drop_columns = list(set(data.columns) - set(cnames))
    data = data.drop(drop_columns, axis = 1)
    return(data)
def load_and_prepare_data(cnames, rename_cols_fct, path):
    data = pd.read_csv(path)
    data = rename_cols_fct(cnames, data)
    data = drop_columns(data, cnames)
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
def rename_cols_temporary_expos(cnames, data):
    data = data.rename(columns={'Any':cnames[10], 'Latitud':cnames[0], 'Longitud': cnames[1],
                                   'Web': cnames[7], 'Seu': cnames[11]})
    return(data)
def rename_cols_exceed(cnames, data):
    data = data.rename(columns={'description':cnames[12], 'start time':cnames[4], 'place': cnames[11],
                                'musice style': cnames[6], 'price': cnames[13]})
    return(data)
def write_db(data, data_name, collection):
    try:
        collection.insert_many(data.to_dict("records"))
        print("%s data successfully written to DB!!!" % data_name)
    except pymongo.errors.WriteError as e:
        print("Could not write %s data to DB: %s" % (data_name, e))