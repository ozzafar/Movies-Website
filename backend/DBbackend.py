import mysql.connector
from mysql.connector import errorcode


class DBbackend:
    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(user='DbMysql06', database='DbMysql06', password='DbMysql06',
                                               host='127.0.0.1', port=3305)
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

    def execute_sql(self, sql, values):
        cursor = self.cnx.cursor()  # get the cursor
        cursor.execute(sql, values)
        self.cnx.commit()

    def insert_movie(self, mv):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "INSERT INTO Movies (movie_ID,title,released,run_time,plot,budget,revenue) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        runtime = mv.runtime
        if runtime != None:
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
        values = (mv.id, mv.title, release_date, runtime, overview, budget, revenue)
        cursor.execute(sql, values)
        self.cnx.commit()

    def insert_rating(self, rating):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "INSERT INTO Rated (rated) VALUES (%s)"
        values = (rating,)
        cursor.execute(sql, values)
        self.cnx.commit()

    def insert_genre(self, g):
        sql = "INSERT INTO Genres (genre) VALUES (%s)"
        values = (g,)
        self.execute_sql(sql, values)

    def insert_countrie(self, c):
        sql = "INSERT INTO Production_Countries (country) VALUES (%s)"
        values = (c,)
        self.execute_sql(sql, values)

    def update_poster(self, url, id):
        sql = "UPDATE Movies SET poster_URL=%s WHERE movie_ID = %s"
        values = (url, id)
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

    def insert_actor(self, first, last, gender):
        sql = "INSERT INTO Person (first_name,last_name,gender) VALUES (%s,%s,%s)"
        values = (first, last, gender)
        self.execute_sql(sql, values)

    def get_movie_ids(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "SELECT movie_ID FROM Movies"
        cursor.execute(sql)
        return cursor.fetchall()

