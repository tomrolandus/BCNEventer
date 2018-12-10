

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
def set_ratings_of_new_user(new_user_id):
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

def generate_user_item_matrix():
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

def generate_random_ratings(df, fill_factor = 1/2):

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


def pearson_similarity(DataFrame, User1, User2, min_common_items=0):
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


def get_most_similar_users(df_old_users, df_new_user, n = 5):

    df_new_user = df_new_user.drop('category_id', axis = 1)
    df_new_user = df_new_user.loc[~np.isnan(df_new_user.rating)]
    df = pd.concat([df_old_users, df_new_user], axis=0)
    new_user_id = df_new_user.user_id.loc[0]

    sim = {}
    for user in df_old_users.user_id.unique():
        sim[user] = pearson_similarity(df, user, new_user_id)

    output = pd.DataFrame({
        'user_id': list(sim.keys()),
        'similarity': list(sim.values())
    }).sort_values('similarity', ascending=False)
    return output.iloc[:n]['user_id']

def get_possible_events(df_new_user):
    possible_events = df_new_user.loc[np.isnan(df_new_user.rating), 'event_id']
    return possible_events

def recommend_events(df_old_users, df_new_user, num_events = 5):

    most_similar_users = get_most_similar_users(df_old_users, df_new_user)
    possible_events = get_possible_events(df_new_user)

    mask1 = df_old_users.event_id.isin(possible_events)

    recommended_events = []
    for user in most_similar_users:
        mask2 = df_old_users.user_id == user
        events = df_old_users.loc[mask1 & mask2, 'event_id']
        for event in events:
            recommended_events.append(event)
            if len(recommended_events) > num_events + 1:
                return recommended_events


#%%
df = generate_user_item_matrix()
df = generate_random_ratings(df)
df_new_user = set_ratings_of_new_user('5c0ce7b951f5a0af4e8da06d')
print(recommend_events(df, df_new_user, 3))

#%%