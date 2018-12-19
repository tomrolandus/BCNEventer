
# TODO: fix geocoding

#%% Modules
import scripts.library as lib
import sys
sys.path.append('../')


from flask import Flask
from flask_mongoengine import MongoEngine

from app.models.category import Category

#%% Parameters
write_production = False
if len(sys.argv) == 2 and sys.argv[1] == 'production':
    # calling script with 'python <script.py> production' will write to the prod_db
    write_production = True

cnames = [
    'name', # 0
    'description', #1
    'location', #2
    'date_time', #3
    'category_ids' #4
]

#%% Connect to db
app = Flask(__name__)
app.config['MONGODB_DB'] = 'bcneventer'
if write_production:
    with open("../credentials.txt", 'r', encoding='utf-8') as f:
        [name, password, url, dbname] = f.read().splitlines()
    app.config['MONGODB_HOST'] = "mongodb://{}:{}@{}/{}".format(name, password, url, dbname)
    print("Connected successfully!!!")
    query_category_ids_from_prod = True
else:
    app.config['MONGODB_HOST'] = "mongodb://localhost:27017/bcneventer"
    print("Connected successfully!!!")
    query_category_ids_from_prod = False
db = MongoEngine(app)

## Xceed
xceed = lib.load_and_prepare_data(cnames,
                                  lib.format_cols_exceed,
                                  "datasets/Xceed/xceed_barcelona.csv",
                                  cat_ids_from_prod = query_category_ids_from_prod)
lib.write_df_to_db(xceed)

print("Finished with Xceed, continue with Meetup...")

#%% Meetup
meetup = lib.load_and_prepare_data(cnames,
                                   lib.format_cols_meetup,
                                   "datasets/MeetUp/events_Barcelona.csv",
                                   delimiter_ = ";",
                                   cat_ids_from_prod = query_category_ids_from_prod)
lib.write_df_to_db(meetup)



