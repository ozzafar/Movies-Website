from config import *
from mysql.connector import errorcode
import mysql.connector


class DBConstructor:
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

    def insert_movie(self, mv):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "INSERT INTO Movies100 (movie_ID,title,released,run_time,plot,budget,revenue,poster_URL,trailer_URL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        runtime = mv.runtime
        if runtime is not None:
            runtime = '{:02d}:{:02d}'.format(*divmod(mv.runtime, 60))
        if runtime == '':
            runtime = None
        budget = mv.budget
        if budget == 0:
            budget = None
        revenue = mv.revenue
        if revenue == 0:
            revenue = None
        overview = mv.overview
        if overview == "" or overview == '':
            overview = None
        release_date = mv.release_date
        if release_date == '':
            release_date = None
        poster = mv.poster_path
        if poster == '':
            poster = None
        trailer = mv.trailers
        if trailer != None and "youtube" in trailer:
            trailer = trailer["youtube"]
            if len(trailer) > 0:
                trailer = trailer[0]["source"]
            else:
                trailer = None
        values = (mv.id, mv.title, release_date, runtime, overview, budget, revenue, poster, trailer)
        cursor.execute(sql, values)
        self.cnx.commit()

    def insert_rating(self, rating):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "INSERT INTO Rated1 (rated) VALUES (%s)"
        values = (rating,)
        cursor.execute(sql, values)
        self.cnx.commit()

    def insert_genre(self, g):
        sql = "INSERT INTO Genres1 (genre) VALUES (%s)"
        values = (g,)
        self.execute_sql(sql, values)

    def insert_countrie(self, c):
        sql = "INSERT INTO Production_Countries1 (country) VALUES (%s)"
        values = (c,)
        self.execute_sql(sql, values)

    def insert_movies_genres(self, m_id, g_id):
        sql = "INSERT INTO Movie_Genres1 (movie_ID,genre_ID) VALUES (%s,%s)"
        values = (m_id, g_id)
        self.execute_sql(sql, values)

    def insert_movies_companies(self, m_id, c_id):
        sql = "INSERT INTO Movie_Companies1 (movie_ID,prod_company_ID) VALUES (%s,%s)"
        values = (m_id, c_id)
        self.execute_sql(sql, values)

    def insert_company(self, c):
        sql = "INSERT INTO Production_companies1 (company) VALUES (%s)"
        values = (c,)
        self.execute_sql(sql, values)

    def insert_actor(self, first, last, gender, profile_path):
        sql = "INSERT INTO Person1 (first_name,last_name,gender,picture_URL) VALUES (%s,%s,%s,%s)"
        values = (first, last, gender, profile_path)
        self.execute_sql(sql, values)

    def insert_country(self, c):
        sql = "INSERT INTO Production_Countries1 (country) VALUES (%s)"
        values = (c,)
        self.execute_sql(sql, values)

    def insert_movies_countries(self, m_id, c_id):
        sql = "INSERT INTO Movie_Countries1 (movie_ID,prod_country_ID) VALUES (%s,%s)"
        values = (m_id, c_id)
        self.execute_sql(sql, values)

    def insert_movies_actors(self, m_id, c_id, character):
        sql = "INSERT INTO Movies_Actors1 (person_ID,movie_ID,figure) VALUES (%s,%s,%s)"
        values = (c_id, m_id, character)
        self.execute_sql(sql, values)

    def insert_movies_crew(self, m_id, c_id, job):
        sql = "INSERT INTO Movies_Crew1 (person_ID,movie_ID,role) VALUES (%s,%s,%s)"
        values = (c_id, m_id, job)
        self.execute_sql(sql, values)

    def insert_score(self, m_id, imdb, rotten_tomatoes, metacritic, imdbVotes):
        sql = "INSERT INTO Movie_Score1 (movie_ID,rotten_tomatoes,metacritic,imdb,imdbVotes) VALUES (%s,%s,%s,%s,%s)"
        values = (m_id, rotten_tomatoes, metacritic, imdb, imdbVotes)
        self.execute_sql(sql, values)

    # endregion

    # region UPDATE

    def update_poster(self, url, id):
        sql = "UPDATE Movies100 SET poster_URL=%s WHERE movie_ID = %s"
        values = (url, id)
        self.execute_sql(sql, values)

    def update_movie(self, m_id, awards, rated):
        sql = "UPDATE Movies100 SET awards=%s, rated_ID=%s WHERE movie_ID = %s"
        values = (awards, rated, m_id)
        self.execute_sql(sql, values)

    # endregion

    # region GETTERS

    def get_genres(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql ="SELECT * FROM Genres1"
        cursor.execute(sql)
        return cursor.fetchall()

    def get_countries(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql ="SELECT * FROM Production_Countries1"
        cursor.execute(sql)
        return cursor.fetchall()

    def get_movie_ids(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "SELECT movie_ID FROM Movies100"
        cursor.execute(sql)
        return cursor.fetchall()