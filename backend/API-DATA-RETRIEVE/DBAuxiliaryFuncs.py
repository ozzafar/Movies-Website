from backend.config import *
from mysql.connector import errorcode
import mysql.connector

""" This class has some duplicate-code of DBbackend.py because we 
assume this repo should be executed independently """

class DBAuxiliaryFuncs:
    # constructor
    def __init__(self):
        try:
            host = '127.0.0.1'
            port = 3305
            if REMOTE:
                host = DB_HOST
                port = DB_PORT
            self.cnx = mysql.connector.connect(user='DbMysql06', database='DbMysql06', password='DbMysql06',
                                               host=host, port=port)
            self.status = True
        except mysql.connector.Error as err:
            self.status = False
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close(self):
        self.cnx.close()

    def execute_sql(self, sql, values=None):
        cursor = self.cnx.cursor()  # get the cursor
        if values is None:
            cursor.execute(sql)
            # changed to fetching all rows and returning them because cursor.execute returns None
            rows = cursor.fetchall()
            return rows
        else:
            cursor.execute(sql, values)
            self.cnx.commit()

    # region INSERT

    def insert_movie_table(self, tmdb_mv, omdb_mv):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "INSERT INTO Movies (movie_ID, title, rated_id, released, run_time, plot, awards, budget, revenue, " \
              "poster_URL, trailer_URL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        rated_id = self.__get_rated_id(omdb_mv)
        runtime = '{:02d}:{:02d}'.format(*divmod(tmdb_mv.runtime, 60))
        plot = self.__get_plot(tmdb_mv, omdb_mv)
        awards = self.__get_awards(omdb_mv)
        revenue = tmdb_mv.revenue
        if revenue is None or revenue == 0:
            revenue = None
        poster = tmdb_mv.poster_path
        if poster is None or poster == '':
            poster = None
        trailer = tmdb_mv.trailers
        if trailer is not None and "youtube" in trailer:
            trailer = trailer["youtube"]
            if len(trailer) > 0:
                trailer = trailer[0]["source"]
            else:
                trailer = None
        values = (tmdb_mv.id, tmdb_mv.title, rated_id, tmdb_mv.release_date, runtime,
                  plot, awards, tmdb_mv.budget, revenue, poster, trailer)
        cursor.execute(sql, values)
        self.cnx.commit()

    def __get_rated_id(self, omdb_mv):
        content_rating = {"G": 1, "PG": 2, "PG-13": 3, "R": 4, "NC-17": 5}
        if omdb_mv["Rated"] in content_rating:
            return content_rating[omdb_mv["Rated"]]
        return None

    def __get_plot(self, tmdb_mv, omdb_mv):
        omdb_plot = omdb_mv['Plot']
        if omdb_plot is not None and len(omdb_plot) > 5:
            return omdb_plot
        return tmdb_mv.overview

    def __get_awards(self, omdb_mv):
        tmp = omdb_mv['Awards']
        if "wins" in tmp:
            tmp = tmp.split()
            if "wins" in tmp:
                wins = tmp[tmp.index("wins") - 1]
            elif "wins." in tmp:
                wins = tmp[tmp.index("wins.") - 1]
            else:
                wins = 0
            if wins.isnumeric():
                return int(wins)
        return 0

    def insert_rating(self, rating):
        sql = "INSERT INTO Rated (rated) VALUES (%s)"
        values = (rating,)
        self.execute_sql(sql, values)

    def insert_genre(self, g):
        sql = "INSERT INTO Genres (genre) VALUES (%s)"
        values = (g,)
        self.execute_sql(sql, values)

    def insert_countrie(self, c):
        sql = "INSERT INTO Production_Countries (country) VALUES (%s)"
        values = (c,)
        self.execute_sql(sql, values)

    def insert_movies_genres(self, m_id, g_id):
        sql = "INSERT INTO Movie_Genres (movie_ID,genre_ID) VALUES (%s,%s)"
        values = (m_id, g_id)
        self.execute_sql(sql, values)

    def insert_movies_companies(self, m_id, c_id):
        sql = "INSERT INTO Movie_Companies (movie_ID,prod_company_ID) VALUES (%s,%s)"
        values = (m_id, c_id)
        self.execute_sql(sql, values)

    def insert_company(self, c):
        sql = "INSERT INTO Production_companies (company) VALUES (%s)"
        values = (c,)
        self.execute_sql(sql, values)

    def insert_country(self, c):
        sql = "INSERT INTO Production_Countries (country) VALUES (%s)"
        values = (c,)
        self.execute_sql(sql, values)

    def insert_movies_countries(self, m_id, c_id):
        sql = "INSERT INTO Movie_Countries (movie_ID,prod_country_ID) VALUES (%s,%s)"
        values = (m_id, c_id)
        self.execute_sql(sql, values)

    def insert_person(self, first, last, gender, profile_path):
        sql = "INSERT INTO Person (first_name,last_name,gender,picture_URL) VALUES (%s,%s,%s,%s)"
        values = (first, last, gender, profile_path)
        self.execute_sql(sql, values)

    def insert_movies_actors(self, m_id, c_id, character):
        sql = "INSERT INTO Movies_Actors (person_ID,movie_ID,figure) VALUES (%s,%s,%s)"
        values = (c_id, m_id, character)
        self.execute_sql(sql, values)

    def insert_movies_crew(self, m_id, c_id, job):
        sql = "INSERT INTO Movies_Crew (person_ID,movie_ID,role) VALUES (%s,%s,%s)"
        values = (c_id, m_id, job)
        self.execute_sql(sql, values)

    def insert_score(self, m_id, imdb, rotten_tomatoes, metacritic, imdbVotes):
        sql = "INSERT INTO Movie_Score (movie_ID,rotten_tomatoes,metacritic,imdb,imdbVotes) VALUES (%s,%s,%s,%s,%s)"
        values = (m_id, rotten_tomatoes, metacritic, imdb, imdbVotes)
        self.execute_sql(sql, values)

    # endregion

    # region UPDATE

    def update_poster(self, url, id):
        sql = "UPDATE Movies SET poster_URL=%s WHERE movie_ID = %s"
        values = (url, id)
        self.execute_sql(sql, values)

    def update_movie(self, m_id, awards, rated):
        sql = "UPDATE Movies SET awards=%s, rated_ID=%s WHERE movie_ID = %s"
        values = (awards, rated, m_id)
        self.execute_sql(sql, values)

    # endregion

    # region GETTERS

    def get_genres(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "SELECT * FROM Genres"
        cursor.execute(sql)
        return cursor.fetchall()

    def get_countries(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "SELECT * FROM Production_Countries"
        cursor.execute(sql)
        return cursor.fetchall()

    def get_movie_ids(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "SELECT movie_ID FROM Movies"
        cursor.execute(sql)
        return cursor.fetchall()

    def get_company_id(self, company):
        cursor = self.cnx.cursor()  # get the cursor
        sql = f"""SELECT prod_company_ID FROM Production_companies WHERE company = "{str(company)}" """
        cursor.execute(sql)
        return cursor.fetchall()

    def get_all_company_data(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = f"""SELECT * FROM Production_companies"""
        cursor.execute(sql)
        return cursor.fetchall()

    def get_person_id(self, first_name, last_name):
        cursor = self.cnx.cursor()  # get the cursor
        sql = f"""SELECT person_ID FROM Person WHERE first_name = "{str(first_name)}" AND last_name = "{str(last_name)}" """
        cursor.execute(sql)
        return cursor.fetchall()

    def get_all_person_data(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = f"""SELECT * FROM Person"""
        cursor.execute(sql)
        return cursor.fetchall()
