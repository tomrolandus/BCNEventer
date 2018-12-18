#%% Connect to db
app = Flask(__name__)
app.config['MONGODB_DB'] = 'bcneventer'
write_production = True
if write_production:
    with open("../credentials.txt", 'r', encoding='utf-8') as f:
        [name, password, url, dbname] = f.read().splitlines()
    app.config['MONGODB_HOST'] = "mongodb://{}:{}@{}/{}".format(name, password, url, dbname)
    print("Connected successfully!!!")
else:
    app.config['MONGODB_HOST'] = "mongodb://localhost:27017/bcneventer"
    # print("Connected successfully!!!")
db = MongoEngine(app)
create_users(50)