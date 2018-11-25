
# TODO: fix geocoding
# TODO: convert categories to ids
# TODO: loop oer rows of dataframe in write_db and write each row to the db


#%% Modules
import library as lib
import sys
sys.path.append('./scripts/')

#%% Parameters
cnames = [
    'name', # 0
    'description', #1
    'location', #2
    'date_time', #3
    'category_ids' #4
]

#%% Connect to db and create collection
conn = lib.connect_to_local_db()
db = conn['bcneventer']

#%% Meetup
col_meetup = db.meetup
meetup = lib.load_and_prepare_data(cnames, lib.rename_cols_meetup, "../datasets/MeetUp/events_Barcelona.csv", delimiter_ = ";")
lib.write_db(meetup, "Meetup", col_meetup)

## Xceed
#col_xceed = db.exceed
#xceed = lib.load_and_prepare_data(cnames, lib.rename_cols_exceed, "../datasets/Xceed/xceed_barcelona.csv")
#lib.write_db(xceed, "Xceed", col_xceed)