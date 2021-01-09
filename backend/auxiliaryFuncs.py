import DBbackend
import pageclasses


def query_to_index_movie(user_genres, min_len, max_len, start_year, end_year):
    recommended_movies_data = DBbackend.recommendations_query(user_genres, min_len, max_len, start_year, end_year)
    indexed_movie_arr = []

    for movie in recommended_movies_data:
        indexed_movie = pageclasses.IndexMovie(movie[1], movie[6], movie[2], movie[5])
        indexed_movie_arr.append(indexed_movie)

    return indexed_movie_arr
