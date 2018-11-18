import pandas as pd
import numpy as np


#Create users
RATES = 'Rates'
MOVIES = 'Events'

class User():
    def __init__(self, name):
        self.name = name
        self.ratings = pd.DataFrame({MOVIES : [], RATES : []})
        
    def rate(self, movie, rating):
        try:
            if movie in self.ratings[MOVIES].tolist():
                self.ratings.loc[self.ratings[MOVIES] == movie, RATES] = rating
            else:
                self.ratings.append(pd.Series({MOVIES : movie, RATES : rating}))
        except TypeError:
            self.ratings = self.ratings.append(pd.Series({MOVIES : movie, RATES : rating}), ignore_index=True)
        
    
    def retrieve_rate(self, movie):
        return self.ratings.loc[self.ratings[MOVIES] == movie][RATES]
    
    def retrieve_movies_between(self, minrate, maxrate):
        return self.ratings[ (self.ratings[RATES]< maxrate) & (self.ratings[RATES] > minrate)]
    
    def retrieve_df(self):
        return self.ratings



def create_user(user_name, events):
    np.random.seed(500)
    user = User(user_name)
    for event in events:
        user.rate(event, np.random.uniform(0, 5))
    return user

