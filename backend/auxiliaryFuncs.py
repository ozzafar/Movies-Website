import DBbackend
import pageclasses

def query_to_index_movie(db, user_genres, movie_length, release):
    genres, min_len, max_len, start_year, end_year = parse_index_movie(user_genres, movie_length, release)
    recommended_movies_data = db.recommendations_query(user_genres, min_len, max_len, start_year, end_year)
    indexed_movie_arr = []

    for movie in recommended_movies_data:
        indexed_movie = pageclasses.IndexMovie(movie[1], movie[6], movie[2], movie[5])
        indexed_movie_arr.append(indexed_movie)

    return indexed_movie_arr

def parse_index_movie(user_genres, movie_length, release):
    genres = user_genres.split(',')
    movie_length_list = movie_length.split(',')
    min_len = int(movie_length_list[0])
    max_len = int(movie_length_list[1])
    if release == 'pre':
        start_year = 1900
        end_year = 1980
    elif release == 'old':
        start_year = 1980
        end_year = 2000
    elif release == 'new':
        start_year = 2000
        end_year = 2100
    elif release == 'all':
        start_year = 1900
        end_year = 2100
    else:
        print("Error in function parse_index_movie in auxiliaryFuncs")
        return
    return genres, min_len, max_len, start_year, end_year