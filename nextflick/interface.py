"""
INTERFACE 
- movies with shape (#number of movies, #features(title, year, genres, ...))
- user_item_matrix with shape (#number of users, #number of movies)
- top_list with shape (#number of movies, 2)
- item-item matrix with shape (#number of popular movies, #number of popular movies)
- nmf_model: trained sklearn NMF model
"""

import pandas as pd
import numpy as np
import pickle
from fuzzywuzzy import process
import os
library_path = os.path.dirname(__file__)

user_item_matrix = pd.read_csv(library_path+'/data/user_item_matrix.csv',index_col=0)           # read in from hard-drive
movies = pd.read_csv(library_path+'/data/ml-latest-small/movies.csv')                   # read in from hard-drive
filtered_movies = pd.read_csv(library_path+'/data/filtered_movies.csv',index_col=0)
movie_links = pd.read_csv(library_path+'/data/ml-latest-small/links.csv')
top_list = pd.read_csv(library_path+'/data/top_ratings.csv')                   # read in from hard-drive
item_item_distance_matrix = pd.read_csv(library_path+'/data/item_item_correlations.csv',index_col=0) # read in from hard-drive
with open(library_path+'/data/nmf_model.pickle', 'rb') as file:
    nmf_model = pickle.load(file)                               # read in from hard-drive
# for modelling, we are taking movies which has been rated by more than 100 ppl and we also remove 
# duplicates about 6 in number ,this list has been saved
#filtered_movies = pd.read_csv('./data/filtered_movies.csv')

#print(movies.head())

def get_top_match(movie_title,filtered_movies):
    #movieId,title,genres
    match= process.extractOne(movie_title,filtered_movies)
    return match

def create_user_vector(new_user_ratings,user_item_matrix):
    """
    convert dict of user_ratings to a user_vector.
    movie_dict is the dict of movies(after going through fuzzywuzzy) and corresponding rating given by the user
    it returns the dataframe with length that of filtered movies and rating value only for movies wchich was rated
    others are all NaN
    """
    empty_list = [np.nan]*user_item_matrix.columns.shape[0]
    ratings_dict = dict(zip(user_item_matrix.columns, empty_list))
    for movie, rating in new_user_ratings.items():
        ratings_dict[movie] = rating
    new_user_df = pd.DataFrame(list(ratings_dict.values()), index=user_item_matrix.columns.values)
    #print(new_user_df.head())

    return new_user_df
