import json
import sys

import omdb
from mysql.connector import IntegrityError
from tmdbv3api import TMDb, Movie
from backend.DBbackend import DBbackend

movie_titles = set()
movies = []
movies_tmdb = []
db = DBbackend()

# ------------------ get popular movies titles by TMDB API ------------------
tmdb = TMDb()
tmdb.api_key = "b1319d9182fbc16b74ad682f29067d21"
movie = Movie()
pages = 9835
flag = True
errors = 0

genres = {"Action": 1, "Adventure": 2, "Animation": 3, "Comedy": 4, "Crime": 5, "Documentary": 6, "Drama": 7,
          "Fantasy": 8, "History": 9, "Horror": 10, "Music": 11, "Mystery": 12, "Romance": 13, "Science Fiction": 14,
          "Thriller": 16, "TV Movie": 15, "War": 17, "Western": 18}

companies = {"Warner Bros. Pictures","Cinema Fund","Universal Pictures","Zero Gravity Management","DC Entertainment","Ingenious Media","Walt Disney Pictures"}

if flag:
    moviesss = db.get_movie_ids()
    for i in range(len(moviesss)):
        m = movie.details(moviesss[i][0])
        try:
            for comp in m.production_companies:
                name = comp["name"]
                if name not in companies:
                    db.insert_company(name)
                    companies.add(name)
        except Exception as e:
            print(e)
            errors += 1

        try:
            for g in m.genres:
                db.insert_movies_genres(m.id, genres[g["name"]])
        except Exception as e:
            print(e)
            errors += 1

        try:
            for actor in m.casts["cast"]:
                res = actor["original_name"].split()
                first = res[0]
                if len(res) > 1:
                    last = res[1]
                else:
                    last = ""
                db.insert_actor(first, last, actor["gender"])
        except Exception as e:
            print(e)
            errors += 1
        try:
            for crew in m.casts["crew"]:
                res = crew["original_name"].split()
                first = res[0]
                if len(res) > 1:
                    last = res[1]
                else:
                    last = ""
                db.insert_actor(first, last, crew["gender"])
        except Exception as e:
            print(e)
            errors += 1

        print("finished movie #" + str(i) + " of " + str(pages))
    print("finished insert all movies, total errors number: " + str(errors))

    # ------------------ get popular movies data by OMDB API ------------------
    # i = 0
    # omdb.set_default("apikey", "5987dc54")
    # for title in movie_titles:
    #     content_bytes = omdb.request(t=title).content
    #     mv = json.loads(content_bytes)
    #     movies.append(mv)
    #     if i % 100 == 0:
    #         print("finishedmovies_tmdb movie #" + str(i) + " of " + str(20 * pages))
    #     i += 1

    # ------------------ fill all tables in DB ------------------

db.close()
