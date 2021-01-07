import sys

import omdb
from mysql.connector import IntegrityError
from tmdbv3api import TMDb, Movie
from omdbapi.movie_search import GetMovie
from backend.DBbackend import DBbackend

movie_titles = set()
movies = []
movies_tmdb = []
db = DBbackend()

# ------------------ get popular movies titles by TMDB API ------------------
tmdb = TMDb()
tmdb.api_key = "b1319d9182fbc16b74ad682f29067d21"
movie = Movie()
flag = False
errors = 0

genres = dict()
companies = dict()
countries = dict()
persons = dict()
rateds = {"G": 1, "PG": 2, "PG-13": 3, "R": 4, "NC-17": 5}

# for i in range(1,50):
#     movies = movie.popular(i)
#     for mv in movies:
#         try:
#             mv = movie.details(mv.id)
#             db.insert_movie(mv)
#         except Exception as e:
#             print(e)
#             errors += 1
#     print("finished page #" + str(i) + " of " + str(60))
# print("finished insert all movies, total errors number: " + str(errors))


if flag:
    moviesss = db.get_movie_ids()
    for i in range(len(moviesss)):
        m = movie.details(moviesss[i][0])
        # m2 = GetMovie(title=m.title, api_key='5987dc54')
        # try:
        #     for country in m.production_countries:
        #         name = country["name"]
        #         if name not in countries:
        #             db.insert_country(name)
        #             countries[name] = len(countries)+1
        #         db.insert_movies_countries(m.id, countries[name])
        # except Exception as e:
        #     print(e)
        #     errors += 1
        # try:
        #     for comp in m.production_companies:
        #         name = comp["name"]
        #         if name not in companies:
        #             db.insert_company(name)
        #             companies[name] = len(companies)+1
        #         db.insert_movies_companies(m.id, companies[name])
        # except Exception as e:
        #     print(e)
        #     errors += 1
        #
        # try:
        #     for g in m.genres:
        #         name = g["name"]
        #         if name not in genres:
        #             db.insert_genre(name)
        #             genres[name] = len(genres)+1
        #         db.insert_movies_genres(m.id, genres[name])
        # except Exception as e:
        #     print(e)
        #     errors += 1
        # try:
        #     tomatoes = None
        #     for s in m2.values["Ratings"]:
        #         if s["Source"]=="Rotten Tomatoes":
        #             tomatoes = int(s["Value"][:-1])
        #             break
        #     metascore = None
        #     if "Metascore" in m2.values and m2.values["Metascore"]!= "N/A":
        #         metascore = int(m2.values["Metascore"])
        #     db.insert_score(m.id, int(10 * float(m2.values["imdbRating"])),tomatoes, metascore, int(m2.values["imdbVotes"].replace(',', '')))
        #     rated = None
        #     if "Rated" in m2.values and m2.values["Rated"] != "N/A":
        #         rated = rateds[m2.values["Rated"]]
        #     db.update_movie(m.id, None, rated) # todo what about awards ?
        # except Exception as e:
        #     print(e)
        #     errors += 1
        #
        # try:
        #     for j in range(min(7, len(m.casts["cast"]))):
        #         person = m.casts["cast"][j]
        #         if person["original_name"] not in persons:
        #             res = person["original_name"].split()
        #             first = res[0]
        #             if len(res) > 1:
        #                 last = " ".join(res[1:])
        #             else:
        #                 last = ""
        #             db.insert_actor(first, last, person["gender"], person["profile_path"])
        #             persons[person["original_name"]] = len(persons) + 1
        #         db.insert_movies_actors(m.id, persons[person["original_name"]], person["character"])
        # except Exception as e:
        #     print(e)
        #     errors += 1
        # try:
        #     for crew in m.casts["crew"]:
        #         if crew["job"] == "Director" or crew['job'] == "Writer":
        #             if crew["original_name"] not in persons:
        #                 res = crew["original_name"].split()
        #                 first = res[0]
        #                 if len(res) > 1:
        #                     last = " ".join(res[1:])
        #                 else:
        #                     last = ""
        #                 db.insert_actor(first, last, crew["gender"], crew["profile_path"])
        #                 persons[crew["original_name"]] = len(persons) + 1
        #             db.insert_movies_crew(m.id, persons[crew["original_name"]], crew["job"])
        # except Exception as e:
        #     print(e)
        #     errors += 1

        print("finished movie #" + str(i) + " of " + str(len(moviesss)))
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