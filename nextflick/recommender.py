"""
Contains various recommondation implementations
all algorithms return a list of movieids
"""

import numpy as np
import pandas as pd
from nextflick.interface import movies,nmf_model,user_item_matrix,create_user_vector,item_item_distance_matrix,top_list


# example output of web application
#new_user_movies = {'Titanic (1997)':3,'Jumanji (1995)':4,'Shawshank Redemption, The (1994)':4}

def really_dum_rec(movies):
    return movies.sample(1)

#recommendation = really_dum_rec()
#print(recommendation)

def recommend_random(user_item_matrix, new_user_rating, k=5):
    """
    return k random unseen movies for user 
    """
    new_user_df = create_user_vector(new_user_rating,user_item_matrix)
    not_rated_mask = np.isnan(new_user_df.T.values[0])
    not_rated = user_item_matrix.columns[not_rated_mask]
    not_rated = pd.DataFrame(not_rated)

    return not_rated.sample(k)



def recommend_most_popular(genre_selected, top_list,filtered_movies, k=5):
    """
    return k most popular unseen movies for user
    """
    #new_user_rating is a dictionary
    num_items = 0
    num_iters = -1
    results = []
    while (num_items<=k) and (num_iters<(top_list.shape[0]-1)):
        num_iters += 1
        item = top_list.iloc[num_iters][0]
        movie_genres = filtered_movies[filtered_movies['title']==item]['genres'].values[0]
        genre_present = True in [genre in movie_genres for genre in genre_selected]
        if genre_present == False:
            pass
        else:
            results.append(item)
            num_items +=1
    return results


def recommend_with_NMF(user_item_matrix, new_user_rating, nmf_model, k=5):
    
    """
    NMF Recommender
    INPUT
    - user_vector with shape (1, #number of movies)
    - user_item_matrix
    - trained NMF model

    OUTPUT
    - a list of movieIds
    """
    new_user_df = create_user_vector(new_user_rating,user_item_matrix)
    #print(new_user_df)
    #print(new_user_df.mean())
   
    Q = nmf_model.components_
    
    # initialization - impute missing values  
    new_user_df_filled = new_user_df.fillna(2.5)  
    new_user_df_filled = new_user_df_filled.T
    #print(new_user_df_filled)
    
    # transform user vector into hidden feature space
    P = nmf_model.transform(new_user_df_filled)
    
    # inverse transformation
    predictions = np.dot(P, Q)

    # build a dataframe
    recommendations = pd.DataFrame(predictions, columns = user_item_matrix.columns)

    # discard seen movies and sort the prediction
    not_rated_mask = pd.isnull(new_user_df.T.values[0])
    not_rated = recommendations.columns[not_rated_mask]
    movies_to_recommend = recommendations[not_rated]
    movies_to_recommend = movies_to_recommend.T
    final_df = pd.DataFrame(movies_to_recommend).reset_index()
    final_df.rename(columns={0:'recommendation_ranking'},inplace=True)
    movies_list = final_df.sort_values(by='recommendation_ranking',ascending=False)[0:k]['index']
    movies_list = list(movies_list)
    
    # return a list of movie titles
    return movies_list


def recommend_with_user_similarity(user_item_matrix, user_rating, k=5):
    pass



def similar_movies(movie_title, item_item_distance_matrix,k=5):
    result = item_item_distance_matrix[movie_title].sort_values(ascending=False)[1:k+1].index
    return result



