from flask import Flask, render_template, request, redirect, url_for,jsonify
from nextflick.recommender import really_dum_rec
from nextflick.interface import get_top_match,movies,create_user_vector,user_item_matrix,nmf_model,item_item_distance_matrix,movie_links,filtered_movies,top_list
from nextflick.recommender import recommend_with_NMF,similar_movies,recommend_most_popular
from fuzzywuzzy import process

# here we construct a Flask object and the __name__ sets this script as the root
app = Flask(__name__)

# redirects to specific URLs
# @ is the symbol for decorator 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies/search')
def movie_search():
    #movie1 = request.args['movie1']
    movie_titles = request.args.getlist('movie')
    ratings = request.args.getlist('rating')
    favourite_movie = request.args.get('favourite_movie')
    genres = ['Comedy','Action','Children','Horror','Romance','Thriller','Sci-Fi','Drama']
    genres_selected = []
    if favourite_movie != None:
        movies_list = similar_movies(favourite_movie, item_item_distance_matrix,k=5)
    elif movie_titles != []:
        new_user_rating_dict = dict(zip(movie_titles,ratings))
        #user_vector = create_user_vector(movie_dict,user_item_matrix.columns)
        #print(user_vector)
        movies_list = recommend_with_NMF(user_item_matrix, new_user_rating_dict, nmf_model, k=5)
    else:
        for genre in genres:
            if request.args.get(genre)=="on":
                genres_selected.append(genre)
        movies_list = recommend_most_popular(genres_selected, top_list,filtered_movies)
        
    movieId_list = []
    movieId_tmdbId = []
    for item in movies_list:
        movieId = movies[movies['title'] == item]['movieId'].values[0]
        movieId_list.append(movieId)
        movieId_tmdbId.append(movie_links[movie_links['movieId']==movieId]['tmdbId'].values[0])
    movieid_title_list = [(a,b,c) for a,b,c in zip(movieId_list,movies_list,movieId_tmdbId)]
    return render_template('results.html',movieid_title_list=movieid_title_list)

@app.route('/movie/<int:movie_id>')
def movie_info(movie_id):
    return render_template('movie.html')
    #return f'Checkout this flick: {movie_id}'

@app.route('/search_autocomplete')
def autocomplete():
    matches = process.extractBests(request.args['term'],user_item_matrix.columns,limit=3)
    return jsonify([match[0] for match in matches])


if __name__ == "__main__":
    # runs app and debug=True and ensures that we make changes the web server restarts
    app.run(debug=True)