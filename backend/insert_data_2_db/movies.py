import tmdbv3api
import requests
from DBConstructor import DBConstructor
import mysql.connector
from datetime import datetime as dt

movie_titles = set()
db = DBConstructor()
api_key = "b1319d9182fbc16b74ad682f29067d21"
# omdb_api_key = '5987dc54'
omdb_api_key = '74fb7c6d'
content_rating = {"G": 1, "PG": 2, "PG-13": 3, "R": 4, "NC-17": 5}
errors = {"budget": 0, "genres": 0, "overview": 0, "runtime": 0, "title": 0, "imdb_id": 0, "score": 0}

# ------------------ get popular movies titles by TMDB API ------------------


class FillingTables:
    def __init__(self):
        self._genres = dict()
        self._companies = dict()
        self._countries = dict()
        self._persons = dict()
        self._all_movies_id = set()

    def fill_genres_table(self):
        genres = tmdbv3api.Genre()
        genres.api_key = api_key
        for genre in genres.movie_list():
            db.insert_genre(genre["name"])

    def fill_rated_table(self):
        for rating in content_rating:
            db.insert_rating(rating)

    def fill_production_countries_table(self):
        countries_for_table = tmdbv3api.Configuration()
        countries_for_table.api_key = api_key
        for country in countries_for_table.countries():
            try:
                db.insert_countrie(country["english_name"])
            except mysql.connector.errors.IntegrityError as err:
                continue

    def __fill_genres_dict(self):
        for genre in db.get_genres():
            self._genres[genre[1]] = genre[0]

    def __fill_countries_dict(self):
        for country in db.get_countries():
            self._countries[country[1]] = country[0]

    def __fill_companies_dict(self):
        for company in db.get_all_company_data():
            self._companies[company[1].lower()] = company[0]

    def __fill_persons_dict(self):
        for pers in db.get_all_person_data():
            self._persons[pers[1] + " " + pers[2]] = pers[0]

    def __fill_movies_ids_set(self):
        for i in db.get_movie_ids():
            self._all_movies_id.add(i[0])

    def __put_all_data_in_dict(self):
        self.__fill_genres_dict()
        self.__fill_countries_dict()
        self.__fill_companies_dict()
        self.__fill_persons_dict()
        self.__fill_movies_ids_set()

    def __get_tmdb_movie_details_generator(self, stater_page):
        movie = tmdbv3api.Movie()
        movie.api_key = api_key
        for i in range(stater_page, 501):
            page = None
            while page is None:
                try:
                    page = movie.popular(i)
                except:
                    print("---------------connection failed 60---------------")
            for j in range(20):
                details = None
                while details is None:
                    try:
                        details = movie.details(page[j].id)
                    except:
                        print("---------------connection failed 67---------------")
                yield details, i, j

    def fill_all_the_tables(self, stater_page, cr):
        self.__put_all_data_in_dict()
        tmdb_movie_generator = self.__get_tmdb_movie_details_generator(stater_page)
        counter = cr
        num_of_spinning = 0  # TODO DELETE
        while counter < 1000:
            print("numOfSpining: " + str(num_of_spinning))  # TODO DELETE
            num_of_spinning += 1  # TODO DELETE
            print("counter: " + str(counter))  # TODO DELETE
            print("errors: " + str(errors))  # TODO DELETE
            tmdb_movie, page, index = next(tmdb_movie_generator)  # get next movie
            if tmdb_movie.id in self._all_movies_id:
                continue
            if not self.__fill_movie_related_table(tmdb_movie):
                continue
            self.__fill_credit_related_table(tmdb_movie.id)
            self._all_movies_id.add(tmdb_movie.id)
            counter += 1

    def __fill_movie_related_table(self, tmdb_movie):
        # Check that all data exists
        if not self.__check_if_all_tmdb_movie_info_is_valid(tmdb_movie):
            print("__check_if_all_tmdb_movie_info_is_valid: " + str(tmdb_movie.title) + " " + str(tmdb_movie.id))  # TODO DELETE
            return False
        payload = {'i': tmdb_movie.imdb_id, 'plot': 'full', 'r': 'json', 'apikey': omdb_api_key}
        omdb_movie = None
        while omdb_movie is None:
            try:
                omdb_movie = requests.get('http://www.omdbapi.com/', params=payload).json()
            except:
                print("---------------connection failed 96---------------")
        if not self.__check_if_score_data_exists(omdb_movie):
            print("__check_if_score_data_exists: " + str(omdb_movie["Title"]) + " " + str(omdb_movie["imdbID"]))  # TODO DELETE
            errors["score"] += 1  # TODO DELETE
            return False

        # fill the tables
        db.insert_movie_table(tmdb_movie, omdb_movie)
        self.__insert_movies_genres_table(tmdb_movie)
        self.__insert_movies_countries_table(tmdb_movie)
        self.__insert_companies_tables(tmdb_movie)
        self.__insert_movie_score_table(omdb_movie, tmdb_movie)
        return True

    def __check_if_all_tmdb_movie_info_is_valid(self, tmdb_movie):
        if not self.__is_date_valid(tmdb_movie.release_date):
            return False
        elif tmdb_movie.budget is None or tmdb_movie.budget < 10000:
            errors["budget"] += 1  # TODO DELETE
            return False
        elif tmdb_movie.genres is None or len(tmdb_movie.genres) == 0:
            errors["genres"] += 1  # TODO DELETE
            return False
        elif tmdb_movie.overview is None or tmdb_movie.overview == "" or tmdb_movie.overview == " ":
            errors["overview"] += 1  # TODO DELETE
            return False
        elif tmdb_movie.runtime is None or tmdb_movie.runtime < 60:
            errors["runtime"] += 1  # TODO DELETE
            return False
        elif tmdb_movie.title is None or tmdb_movie.title == "" or tmdb_movie.title == " " or \
                len(tmdb_movie.title) >= 200:
            errors["title"] += 1  # TODO DELETE
            return False
        elif tmdb_movie.imdb_id is None or tmdb_movie.imdb_id == "" or tmdb_movie.imdb_id == " ":
            errors["imdb_id"] += 1  # TODO DELETE
            return False
        return True

    def __is_date_valid(self, release_date):
        max_date = dt.strptime("2021-1-1", "%Y-%m-%d")
        if release_date is None or release_date == '' or max_date < dt.strptime(release_date, "%Y-%m-%d"):
            return False
        return True

    def __check_if_score_data_exists(self, omdb_movie):
        score = omdb_movie["Ratings"]
        if len(score) < 3:
            return False
        elif(score[0]['Value'] == '' or score[0]['Value'] is None or
             score[1]['Value'] == '' or score[1]['Value'] is None or
             score[2]['Value'] == '' or score[2]['Value'] is None):
            return False
        return True

    def __insert_movies_genres_table(self, tmdb_movie):  # len(tmdb_movie.genres) > 0
        for g in tmdb_movie.genres:
            name = g["name"]
            db.insert_movies_genres(tmdb_movie.id, self._genres[name])

    def __insert_movies_countries_table(self, tmdb_movie):
        for country in tmdb_movie.production_countries:
            name = country["name"]
            db.insert_movies_countries(tmdb_movie.id, self._countries[name])

    def __insert_companies_tables(self, tmdb_movie):
        for comp in tmdb_movie.production_companies:
            name = comp["name"]
            if name.lower() not in self._companies:
                db.insert_company(name)
                self._companies[name.lower()] = db.get_company_id(name)[0][0]
            db.insert_movies_companies(tmdb_movie.id, self._companies[name.lower()])

    def __insert_movie_score_table(self, omdb_movie, tmdb_movie):
        for s in omdb_movie["Ratings"]:
            if s["Source"] == 'Internet Movie Database':
                imdb_rating = int(10 * float(s["Value"][:-3]))
            elif s["Source"] == "Rotten Tomatoes":
                tomatoes_rating = int(s["Value"][:-1])
            elif s["Source"] == "Metacritic":
                metacritic_rating = int(s["Value"][:-4])
        db.insert_score(tmdb_movie.id, imdb_rating, tomatoes_rating, metacritic_rating,
                        int(omdb_movie["imdbVotes"].replace(',', '')))

    def __fill_credit_related_table(self, movie_id):
        movie = tmdbv3api.Movie()
        movie.api_key = api_key
        staff = None
        while staff is None:
            try:
                staff = movie.credits(movie_id)
            except:
                print("---------------connection failed 186---------------")
        self.__fill_actors_and_person_tables(staff["cast"], movie_id)
        self.__fill_crew_and_persons_table(staff["crew"], movie_id)

    def __fill_actors_and_person_tables(self, cast, movie_id):
        counter = 0
        for ac in cast:
            if counter >= 7:
                break
            name = ac.name
            if name is None or len(name.split()) < 2 or len(name.split()[0]) >= 20 or len(name.split()[1]) >= 20:
                continue
            if name not in self._persons:
                self.__fill_person_table_and_dict(ac)
            figure = ac.character
            if figure is None or len(figure) >= 100:
                figure = ''

            db.insert_movies_actors(movie_id, self._persons[name], figure)
            counter += 1

    def __fill_crew_and_persons_table(self, crew, movie_id):
        director_flag = False
        writer_flag = False

        for cr in crew:
            if director_flag and writer_flag:
                break
            job = cr.job
            if job is not None and ((not director_flag and job == "Director") or (not writer_flag and job == "Writer")):
                name = cr.name
                if name is None or len(name.split()) < 2:
                    continue
                if name not in self._persons:
                    self.__fill_person_table_and_dict(cr)
                db.insert_movies_crew(movie_id, self._persons[name], job)
                if job == "Director":
                    director_flag = True
                else:
                    writer_flag = True

    def __fill_person_table_and_dict(self, per):
        gender = per.gender
        if type(gender) is not int or (gender != 1 and gender != 2):
            gender = 0
        poster = per.profile_path
        if poster is None or len(poster) < 3:
            poster = None
        db.insert_person(per.name.split()[0], per.name.split()[1], gender, poster)
        self._persons[per.name] = db.get_person_id(per.name.split()[0], per.name.split()[1])[0][0]


fill_it = FillingTables()
# fill_it.fill_genres_table()
# fill_it.fill_rated_table()
# fill_it.fill_production_countries_table()

fill_it.fill_all_the_tables(91, 902)

db.close()
