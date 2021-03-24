print("Hello and welcome to NextFlick")

def test_package():
    print('welcome to test_package function')

def open_file(fname):
    """helper function to open a local file"""
    return open(os.path.join(os.path.dirname(__file__), fname))

import os
import pandas as pd
from fuzzywuzzy import process

library_path = os.path.dirname(__file__)
movies = pd.read_csv(library_path+'/data/filtered_movies.csv')

def get_top_matches(query, k=5):
    # [(movieId, title, genres), ...]
    matches = process.extract(query, movies['title'], limit=k)
    return matches