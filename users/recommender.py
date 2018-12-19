# %% LIBRARIES AND CONNECTION TO DB
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from app.models.event import Event
from app.models.user import User


# %% HELPERS TO GET STUFF FROM THE DB
def get_category_ids_of_user(user_id):
    """
    Returns a list with all the category_ids of user (as strins)
    """
    category_ids = [category.id.__str__() for category in User.objects.get(id=user_id).categories]
    return category_ids


def get_event_ids_from_db():
    """
    Returns a list with all the event_ids (as strings)
    """
    event_ids = [event.id.__str__() for event in Event.objects]
    return event_ids


def get_user_ids_from_db():
    """
    Returns a list with all the user_ids (as strings)
    """
    user_ids = [user.id.__str__() for user in User.objects]
    return user_ids


def get_category_id_of_event(event_id):
    """
    Returns first category_id of event (as string)
    """
    event = Event.objects.get(id=event_id)
    return event.categories[0].id.__str__()


def get_event_ids_of_user(user_id):
    """
    Returns a list with all event_ids that the user liked (as strings)
    """
    user = User.objects.get(id=user_id)
    event_ids = [event.id.__str__() for event in user.events]
    return event_ids


def get_event_ids_and_cat_ids_from_db():
    """
    Returns mapping of 'event_id' and 'category' as dataframe
    """
    event_ids = get_event_ids_from_db()
    category_ids = [get_category_id_of_event(event_id) for event_id in event_ids]
    df = pd.DataFrame({
        'event_id': event_ids,
        'category_id': category_ids
    })
    return df


def get_event_ids_of_category(cat_id):
    """
    Returns a list with all event_ids that have given category (as strings)
    """
    events = Event.objects(categories=cat_id)
    event_ids = [event.id.__str__() for event in events]
    return event_ids


# %%
def set_ratings_of_user(user_id):
    """
    This function prepares the dataframe that is necessary to recommend an event to the user
    :param user_id: str
    :return:
    """
    all_events = get_event_ids_from_db()
    user_events = get_event_ids_of_user(user_id=user_id)
    user_categories = get_category_ids_of_user(user_id=user_id)

    # create df with user_id and ALL events
    # and assign 0 rating to all events
    df = pd.DataFrame({
        'user_id': [user_id] * len(all_events),
        'event_id': all_events,
        'rating': [0] * len(all_events)
    })

    # classify all the events that are within the preferred categories of the user
    event_ids = []
    for cat_id in set(user_categories):
        event_ids = event_ids + get_event_ids_of_category(cat_id)

    # set all the events that are within the preferred categories of the user to NaN
    # since the user hasn't rated them yet
    isin_user_categories = df.event_id.isin(set(event_ids))
    df.loc[isin_user_categories, 'rating'] = np.nan

    # then assign 1 to events
    # that the user wants to go to
    isin_user_events = df.event_id.isin(user_events)
    df.loc[isin_user_events, 'rating'] = 1

    return df


# %%


def generate_random_user_item_matrix(user_id, fill_factor=0.2):
    """
    Generates a user-item matrix that is randomly filled with 0's and 1's.
    The ratio of 1's is equal to fill_factor. The matrix does not contain
    the user_id, since the recommender is 'trained' on the other users
    :param user_id:
    :param fill_factor:
    :return:
    """
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
    # remove the user with given user_id from dataframe
    df_users = df_users.loc[df_users.user_id != user_id]

    # do cartesian product of users and events
    df_user_event = pd.merge(df_users, df_events).drop('key', axis=1)
    return generate_random_ratings(df_user_event, fill_factor)
    # return df_user_event


def generate_random_ratings(df, fill_factor):
    """
    Randomly fills df with 0's and 1's. Ratio of 1's is given by fill_factor
    :param df:
    :param fill_factor: float
    :return:
    """
    # get user_item matrix and set indices to 0
    df['rating'] = 0

    # generate positions to fill with rating
    length = df.shape[0]
    indices_all = np.linspace(0, length - 1, length, dtype = int)
    size = int(length * fill_factor)
    indices = np.random.choice(indices_all, size=size)

    # fill with rating = 1
    df['rating'].iloc[indices] = 1
    return df


def pearson_similarity(DataFrame, User1, User2, min_common_items=0):
    """
    Computes the similarity of two users in DataFrame
    :param DataFrame:
    :param User1:
    :param User2:
    :param min_common_items:
    :return:
    """
    # GET events OF USER1
    events_user1 = DataFrame[DataFrame['user_id'] == User1]
    # GET events OF USER2
    events_user2 = DataFrame[DataFrame['user_id'] == User2]

    # find shared events
    rep = pd.merge(events_user1, events_user2, on='event_id')
    if len(rep) == 0:
        return 0
    if len(rep) < min_common_items:
        return 0
    res = pearsonr(rep['rating_x'], rep['rating_y'])[0]
    if np.isnan(res):
        return 0
    return res


def get_most_similar_users(df_old_users, df_new_user, n=5):
    """
    Returns list of n most similar users to user in df_new_user
    :param df_old_users: df
    :param df_new_user: df
    :param n:
    :return: list
    """
    df_new_user = df_new_user.loc[~np.isnan(df_new_user.rating)]
    new_user_id = df_new_user.user_id.iloc[0]

    df = pd.concat([df_old_users, df_new_user], axis=0)

    sim = {}
    for user in df_old_users.user_id.unique():
        sim[user] = pearson_similarity(df, user, new_user_id)

    output = pd.DataFrame({
        'user_id': list(sim.keys()),
        'similarity': list(sim.values())
    }).sort_values('similarity', ascending=False)
    return output.iloc[:n]['user_id']


def get_possible_events(df_new_user):
    """
    Returns all events that can be potentially recommended to the user
    :param df_new_user:
    :return:
    """
    possible_events = df_new_user.loc[np.isnan(df_new_user.rating), 'event_id']
    return possible_events


def recommend_events(df_old_users, df_new_user, num_events=5):
    """
    Returns list of num_events events that are recommended to the user

    The logic is based on finding the most similar users, and recommending an event they
    liked. The restriction is that the recommended event must be within the preferred
    category of the user
    :param df_old_users:
    :param df_new_user:
    :param num_events:
    :return:
    """
    most_similar_users = get_most_similar_users(df_old_users, df_new_user)
    possible_events = get_possible_events(df_new_user)

    mask1 = df_old_users.event_id.isin(possible_events)

    recommended_events = []
    for user in most_similar_users:
        mask2 = df_old_users.user_id == user
        events = df_old_users.loc[mask1 & mask2, 'event_id']
        for event in events:
            recommended_events.append(event)
            if len(recommended_events) >= num_events:
                return recommended_events
    return recommended_events


def set_recommended_events(user_id):
    """
    Gets the recommended events and saves them in the User class
    :param user_id: the id of the current user
    :return: nothing
    """
    print('get new recommended events')
    df_old_users = generate_random_user_item_matrix(user_id)
    df_new_user = set_ratings_of_user(user_id)
    user = User.objects(id=user_id).first()
    user.set_recommended_events(recommend_events(df_old_users, df_new_user))