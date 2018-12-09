

#%%
import pandas as pd
import numpy as np
from scipy.stats import pearsonr


from flask import Flask
from flask_mongoengine import MongoEngine
from app.models.user import User

app = Flask(__name__)
app.config['MONGODB_DB'] = 'bcneventer'
app.config['MONGODB_HOST'] = "mongodb://localhost:27017/bcneventer"

db = MongoEngine(app)

from app.models.event import Event

#%%
def set_ratings_of_new_user(new_user_id, num_events = 10):
    all_events_cats = get_event_ids_and_cat_ids_from_db()
    user_events = get_event_ids_of_user(user_id = new_user_id)
    user_categories = get_category_ids_of_user(user_id = new_user_id)

    # create df with new_user_id and ALL event ids and ALL category ids
    df = pd.DataFrame({
        'user_id': new_user_id,
        'event_id': all_events_cats.event_id,
        'category_id': all_events_cats.category_id
    })

    # assign ratings
    # first assign np.nan to 'rating' column
    df['rating'] = np.nan

    # then assign 0 to events
    # that are not within the preferred categories of the user
    isin_user_categories = df.category_id.isin(user_categories)
    df.loc[~isin_user_categories, 'rating'] = 0

    # then assign 1 to events
    # that the user wants to go
    isin_user_events = df.event_id.isin(user_events)
    df.loc[isin_user_events, 'rating'] = 1
    #[1 for event in df.event_id if event in user_events]
    return df


def get_category_ids_of_user(user_id):
    category_ids = [category.id.__str__() for category in User.objects.get(id=user_id).categories]
    return category_ids

def get_event_ids_from_db():
    event_ids = [event.id.__str__() for event in Event.objects]
    return event_ids

def get_user_ids_from_db():
    user_ids = [user.id.__str__() for user in User.objects]
    return user_ids

def get_category_id_of_event(event_id):
    # This takes only the first category of every event
    event = Event.objects.get(id=event_id)
    return event.categories[0].id.__str__()

def get_event_ids_of_user(user_id):
    user = User.objects.get(id=user_id)
    event_ids = [event.id.__str__() for event in user.events]
    return event_ids

def get_event_ids_and_cat_ids_from_db():
    event_ids = get_event_ids_from_db()
    category_ids = [get_category_id_of_event(event_id) for event_id in event_ids]
    df = pd.DataFrame({
        'event_id': event_ids,
        'category_id': category_ids
    })
    return df

def generate_training_matrix():
    # generate df with events_ids and temporary key for doing cartesian product with user_ids
    df_events = pd.DataFrame({
        'key': 1,
        'event_id': get_event_ids_from_db()
    })
    # generate df with user_ids and temporary key for doing cartesian product with events_ids
    df_users = pd.DataFrame({
        'key': 1,
        'user_id': get_user_ids_from_db()
    })
    # do cartesian product of users and events
    df_user_event = pd.merge(df_users, df_events).drop('key', axis = 1)
    return df_user_event

def generate_random_ratings(df, fill_factor = 1/3):

    # get user_item matrix and set indices to 0
    df['rating'] = 0

    # generate positions to fill with rating
    length = df.shape[0]
    indices_all = np.linspace(0, length-1, length, dtype = int)
    size = int(length*fill_factor)
    indices = np.random.choice(indices_all, size = size)

    # fill with rating = 1
    df['rating'].iloc[indices] = 1
    return df


def pearson_similarity(DataFrame, User1, User2, min_common_items=1):
    # GET event OF USER1
    events_user1 = DataFrame[DataFrame['user_id'] == User1]
    # GET events OF USER2
    events_user2 = DataFrame[DataFrame['user_id'] == User2]

    # find shared events
    rep = pd.merge(events_user1, events_user2, on='event_id')
    if len(rep) == 0:
        return 0
    if (len(rep) < min_common_items):
        return 0
    res = pearsonr(rep['rating_x'], rep['rating_y'])[0]
    if (np.isnan(res)):
        return 0
    return res

#%%
class CollaborativeFiltering:
    """ Collaborative filtering using a custom sim(u,u'). """

    def __init__(self, DataFrame, similarity=pearson_similarity):
        """ Constructor """
        self.sim_method = similarity  # Gets recommendations for a person by using a weighted average
        self.df = DataFrame
        self.sim = pd.DataFrame(np.sum([0]), columns=DataFrame.user_id.unique(), index=DataFrame.user_id.unique())

    def learn(self):
        """ Prepare data structures for estimation. Similarity matrix for users """
        allUsers = set(self.df['user_id'])
        self.sim = {}
        for person1 in allUsers:
            self.sim.setdefault(person1, {})
            a = self.df[self.df['user_id'] == person1][['event_id']]
            data_reduced = pd.merge(self.df, a, on='event_id')
            for person2 in allUsers:
                if person1 == person2: continue
                self.sim.setdefault(person2, {})
                if (person1 in self.sim[person2]): continue  # since it is a symmetric matrix
                sim = self.sim_method(data_reduced, person1, person2)
                if (sim < 0):
                    self.sim[person1][person2] = 0
                    self.sim[person2][person1] = 0
                else:
                    self.sim[person1][person2] = sim
                    self.sim[person2][person1] = sim

    def estimate(self, user_id, event_id):
        totals = {}
        event_users = self.df[self.df['event_id'] == event_id]
        rating_num = 0.0
        rating_den = 0.0
        allUsers = set(event_users['user_id'])
        for other in allUsers:
            if user_id == other: continue
            rating_num += self.sim[user_id][other] * float(event_users[event_users['user_id'] == other]['rating'])
            rating_den += self.sim[user_id][other]

        if rating_den == 0:
            if self.df.rating[self.df['event_id'] == event_id].mean() > 0:
                # return the mean event rating if there is no similar for the computation
                return self.df.rating[self.df['event_id'] == event_id].mean()
            else:
                # else return mean user rating
                return self.df.rating[self.df['user_id'] == user_id].mean()
        return rating_num / rating_den

    def get_sim(self):
        return self.sim

#%%
if __name__ == "__main__":
    #df = generate_training_matrix()
    #df = generate_random_ratings(df)
    #recsys = CollaborativeFiltering(df)
    #recsys.learn()
    #recsys.get_sim()
    print(get_event_ids_and_cat_ids_from_db())

#%%


#%%
for el in nones:
    if el != None:
        print(el)

#%%