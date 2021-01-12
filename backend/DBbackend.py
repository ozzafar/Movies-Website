import mysql.connector
from mysql.connector import errorcode
from config import *

MIN_YEAR = 1900
MAX_YEAR = 2100
ALL = "*"


class DBbackend:

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

    def insert_rated(self, rated_id, rated):
        sql = "INSERT INTO Rated (rated_ID,rated) VALUES (%s,%s)"
        values = (rated_id, rated)
        self.execute_sql(sql, values)


    def insert_movie(self, mv, awards):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "INSERT INTO Movies (movie_ID,title,released,run_time,plot,budget,revenue,poster_URL,trailer_URL,awards) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
        values = (mv.id, mv.title, release_date, runtime, overview, budget, revenue, poster, trailer, awards)
        cursor.execute(sql, values)
        self.cnx.commit()

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

    def insert_actor(self, first, last, gender, profile_path):
        sql = "INSERT INTO Person (first_name,last_name,gender,picture_URL) VALUES (%s,%s,%s,%s)"
        values = (first, last, gender, profile_path)
        self.execute_sql(sql, values)

    def insert_country(self, c):
        sql = "INSERT INTO Production_Countries (country) VALUES (%s)"
        values = (c,)
        self.execute_sql(sql, values)

    def insert_movies_countries(self, m_id, c_id):
        sql = "INSERT INTO Movie_Countries (movie_ID,prod_country_ID) VALUES (%s,%s)"
        values = (m_id, c_id)
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

    def update_movie(self, m_id, rated):
        sql = "UPDATE Movies SET rated_ID=%s WHERE movie_ID = %s"
        values = (rated, m_id)
        self.execute_sql(sql, values)

    # endregion

    # region SELECT

    def get_movie_ids(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "SELECT movie_ID FROM Movies"
        cursor.execute(sql)
        return cursor.fetchall()

    def get_actors(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "SELECT * FROM Person"
        cursor.execute(sql)
        return cursor.fetchall()

    def get_movies(self):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "SELECT * FROM Movies"
        cursor.execute(sql)
        return cursor.fetchall()

    def get_movie(self,m_id):
        cursor = self.cnx.cursor()  # get the cursor
        sql = "SELECT * FROM Movies WHERE movie_ID=%s"
        cursor.execute(sql,(m_id,))
        return cursor.fetchall()

    #endregion

    # region Queries

    # user_genres is an array
    # Opening page
    def recommendations_query(self, user_genres, min_len, max_len, start_year, end_year):
        user_genres_string = self.parse_genres("g", user_genres)

        query = f"""
        SELECT rmn.movie_ID, rmn.title, GROUP_CONCAT(rmn.genre), rmn.released, rmn.run_time, rmn.popularity, rmn.poster_URL
        FROM(
            SELECT g.genre, m.movie_ID, m.title, m.released, m.run_time,
              (ms.rotten_tomatoes+ms.metacritic+ms.imdb)/3 AS popularity,
              ROW_NUMBER() OVER(Partition BY g.genre ORDER BY (ms.rotten_tomatoes+ms.metacritic+ms.imdb)/3 DESC) AS popularity_rank,
              m.poster_URL
            FROM Movies m, Movie_Genres mg, Genres g, Movie_Score ms
            WHERE m.movie_ID = mg.movie_ID AND mg.genre_ID = g.genre_ID
            AND ({user_genres_string}) AND m.movie_ID = ms.movie_ID
            AND EXTRACT(YEAR FROM m.released) BETWEEN {start_year} AND {end_year}
            AND (EXTRACT(HOUR FROM m.run_time)*60+EXTRACT(MINUTE FROM m.run_time))
        	BETWEEN {min_len} AND {max_len}
            ) rmn
        WHERE rmn.popularity_rank <= 10
        GROUP BY rmn.movie_ID, rmn.title, rmn.released, rmn.run_time, rmn.popularity
        ORDER BY rmn.popularity DESC
        """

        rows = self.execute_sql(query)
        return rows

    # If user doesn't specifies user_genre - return all categories. Same with years
    # TODO - delete. not in use
    def popular_movies_query(self, user_genre, start_year, end_year):
        query = f"""
        SELECT m.title, g.genre, m.released, m.run_time, m.plot, (ms.rotten_tomatoes+ ms.metacritic+ ms.imdb)/3 AS popularity, r.rated
        FROM Movies m, Movie_Score ms, Movie_Genres mg, Genres g, Rated r
        WHERE m.movie_ID = ms.movie_ID AND EXTRACT(YEAR FROM m.released) BETWEEN {start_year} AND {end_year} AND m.movie_ID = mg.movie_ID
            AND mg.genre_ID = g.genre_ID AND g.genre = {user_genre} AND m.rated_ID = r.rated_ID
        ORDER BY popularity DESC
        """
        rows = self.execute_sql(query)
        return rows

    # Celebrities grid
    def popular_actors_query(self, movie_score, start_year, end_year):

        query = f"""
        SELECT p.person_ID, p.first_name, p.last_name, p.gender, COUNT(*) AS amount_of_movies, p.picture_URL
        FROM Person p, Movies_Actors ma, Movie_Score ms, Movies m
        WHERE p.person_ID = ma.person_ID AND ma.movie_ID = ms.movie_ID AND ma.movie_ID=m.movie_ID
        	  AND EXTRACT(YEAR FROM m.released) BETWEEN {start_year} AND {end_year}
            AND (ms.rotten_tomatoes +  ms.metacritic + ms.imdb)/3 >= {movie_score}

        GROUP BY p.person_ID, p.first_name, p.last_name, p.picture_URL
        ORDER BY amount_of_movies DESC
        """

        rows = self.execute_sql(query)
        return rows

    # Celebrities grid
    def popular_crew_query(self, movie_score, start_year, end_year):

        query = f"""
        SELECT p.person_ID, p.first_name, p.last_name, p.gender, COUNT(*) AS amount_of_movies,
              p.picture_URL, GROUP_CONCAT(DISTINCT mc.role SEPARATOR ", ")
        FROM Person p, Movies_Crew mc, Movie_Score ms, Movies m
        WHERE p.person_ID = mc.person_ID AND mc.movie_ID = ms.movie_ID AND mc.movie_ID=m.movie_ID
        	  AND EXTRACT(YEAR FROM m.released) BETWEEN {start_year} AND {end_year}
            AND (ms.rotten_tomatoes +  ms.metacritic + ms.imdb)/3 >= {movie_score}

        GROUP BY p.person_ID, p.first_name, p.last_name, p.picture_URL
        ORDER BY amount_of_movies DESC
        """

        rows = self.execute_sql(query)
        return rows

    # Fun Facts
    def director_actor_coupling_query(self, number_of_movies, user_genres):
        user_genres_string = self.parse_genres("dagm", user_genres)

        query = f"""
        SELECT director_ID, director_first_name, director_last_name, director_pic, actor_ID, actor_first_name, 
            actor_last_name, actor_pic, SUM(co_operations) AS co_operations, GROUP_CONCAT(genre SEPARATOR "<br>") AS user_genres
        FROM Director_Actor_Genre_NumOfMovies dagm
        WHERE ({user_genres_string})
        GROUP BY director_ID, director_first_name, director_last_name, actor_ID, actor_first_name, actor_last_name
        HAVING co_operations >= {number_of_movies}
        ORDER BY co_operations DESC
        """

        rows = self.execute_sql(query)
        return rows

    # Fun Facts
    def directors_movies_budget_query(self, budget, actors_number=1):

        query = f"""
        SELECT t.person_ID, t.first_name AS director_first_name, t.last_name AS director_last_name,
            t.picture_URL AS director_picture, t.movie_ID, t.title, t.num_of_actors, t.budget, t.total_budget,
            t.poster_URL AS movie_poster, t.movie_index, t.max_index
        FROM (
            SELECT person_ID, first_name, last_name, title, num_of_actors, budget, picture_URL, poster_URL,
                movie_ID, 
                SUM(budget) OVER (PARTITION BY person_ID, first_name, last_name, picture_URL) total_budget,
                ROW_NUMBER() OVER (PARTITION BY person_ID, first_name, last_name, picture_URL ORDER BY budget DESC) movie_index,
                COUNT(*) OVER (PARTITION BY person_ID, first_name, last_name, picture_URL) max_index
            FROM Movie_numOfActors_Director mad
            WHERE mad.num_of_actors >={actors_number} AND mad.budget>=10000 # TODO delete last condition
          ) t
        WHERE t.total_budget>={budget}
        ORDER BY director_first_name, director_last_name, budget DESC
        """

        rows = self.execute_sql(query)
        return rows

    # TODO - delete. no need in this query
    # return Director-total_budget (total_budget is the total_budget of movies made by the director, each having more that "num_of_actors" played in)
    def directors_budget_query(self, budget, num_of_directors=10, num_of_actors=1):
        pass

        # WORKING

        # query = f"\
        # SELECT person_ID, first_name, last_name, SUM(budget) AS total_budget
        # FROM Movie_numOfActors_Director mad
        # WHERE mad.num_of_actors >={num_of_actors}
        # GROUP BY person_ID, first_name, last_name
        # HAVING total_budget>={budget}
        # ORDER BY total_budget DESC
        # LIMIT {num_of_directors}"

        # rows = self.execute_sql(query)
        # return rows

    # user can ignore awards
    # Fun Facts
    def countries_movies_query(self, movie_budget, movie_awards=0):

        query = f"""
        SELECT cmn.country, cmn.movie_ID, cmn.title, cmn.budget, cmn.awards, cmn.poster_URL AS movie_poster
        FROM(
            SELECT pc.country, m.title, m.budget, m.awards, m.poster_URL, m.movie_ID,
                ROW_NUMBER() OVER(Partition BY pc.country
                ORDER BY m.budget, m.awards DESC) AS ranked_budget
            FROM Production_Countries pc, Movie_Countries mc, Movies m
            WHERE pc.prod_country_ID = mc.prod_country_ID AND mc.movie_ID = m.movie_ID
                        AND m.budget >= {movie_budget} AND m.awards >= {movie_awards}
            ) cmn
        WHERE cmn.ranked_budget <= 10 # for each country return only 10 countries
        ORDER BY cmn.country, cmn.awards DESC, cmn.budget DESC
        """

        rows = self.execute_sql(query)
        return rows

    # Fun Facts
    def actors_movies_awards_query(self, start_year):

        query = f"""
        SELECT p.first_name, p.last_name, p.gender, COUNT(*) AS number_of_movies_played ,
        	SUM(m.awards) AS total_awards
        FROM Person p, Movies_Actors ma, Movies m
        WHERE p.person_ID = ma.person_ID AND ma.movie_ID = m.movie_ID
            AND EXTRACT(YEAR FROM m.released) > {start_year}
        GROUP BY p.person_ID, p.first_name, p.last_name, p.gender
        ORDER BY total_awards DESC, number_of_movies_played DESC
        """

        rows = self.execute_sql(query)
        return rows

    # ------ Full-Text Queries --------

    # TODO - ask dvir if he wants to make it available to choose soome categories or just (one or all)
    # TODO either way need to handle the oprion of "ALL"
    # Movies Grid
    def movies_with_string_in_name_query(self, string_to_search, movie_score, user_genres, start_year,
                                         end_year, sub_string=False):
        string_to_search_arr = string_to_search.split(" ")
        if len(string_to_search_arr) == 1:
            string_to_search = "+" + string_to_search
            if sub_string:
                string_to_search = string_to_search + "*"
        else:
            for i,string in enumerate(string_to_search_arr):
                string_to_search_arr[i] = "+" + string_to_search_arr[i]
                if sub_string:
                    string_to_search_arr[i] = string_to_search_arr[i] + "*"
            string_to_search = " ".join(string_to_search_arr)


        user_genres_string = self.parse_genres("g", user_genres)

        query = f"""
        SELECT m.movie_ID, m.title, GROUP_CONCAT(g.genre), (ms.rotten_tomatoes +  ms.metacritic + ms.imdb)/3 AS popularity, m.poster_URL
        FROM Movies m, Movie_Score ms, Movie_Genres mg, Genres g
        WHERE Match(m.title) AGAINST("{string_to_search}" IN BOOLEAN MODE)
              AND m.movie_ID = ms.movie_ID
              AND (ms.rotten_tomatoes +  ms.metacritic + ms.imdb)/3 >= {movie_score}
              AND m.movie_ID = mg.movie_ID AND mg.genre_ID = g.genre_ID AND ({user_genres_string})
              AND EXTRACT(YEAR FROM m.released) BETWEEN {start_year} AND {end_year}
        GROUP BY m.movie_ID, m.title, popularity, m.poster_URL
        ORDER BY popularity DESC
        """
        rows = self.execute_sql(query)
        return rows

    # TODO - delete. not using this query
    def movies_with_string_in_plot_query(self, string_to_search, sub_string=False):
        pass

        # WORKING

        # if sub_string:
        #     string_to_search = string_to_search + "*"
        #
        # query = f"\
        # SELECT m.title, r.rated, m.released, m.run_time, m.plot, m.awards, m.budget, m.revenue\
        # FROM Movies m, Rated r\
        # WHERE m.rated_ID = r.rated_ID AND Match(m.plot) AGAINST(\"{string_to_search}\" IN BOOLEAN MODE)"
        #
        # rows = self.execute_sql(query)
        # return rows

    # Fun Facts/Movies Grid
    def movies_actors_with_string_in_name_query(self, string_to_search, sub_string=False):

        if sub_string:
            string_to_search = string_to_search + "*"

        query = f"""
        SELECT m.movie_ID, m.title, COUNT(*) as num_of_actors, 
            GROUP_CONCAT(concat(p.first_name, " "), p.last_name SEPARATOR ", ")
        FROM Movies m, Movies_Actors ma, Person p
        WHERE m.movie_ID = ma.movie_ID AND p.person_ID = ma.person_ID
            AND (Match(p.first_name) AGAINST("{string_to_search}" IN BOOLEAN MODE) OR
                Match(p.last_name) AGAINST("{string_to_search}" IN BOOLEAN MODE))
        GROUP BY m.movie_ID, m.title
        ORDER BY num_of_actors DESC
        """

        rows = self.execute_sql(query)
        return rows

    # endregion

    # region Auxiliary_Funcs

    def parse_genres(self, table_name, user_genres):
        string = ""

        for i, genre in enumerate(user_genres):
            string = string + f"""{table_name}.genre = "{genre}" """
            if i < len(user_genres) - 1:
                string = string + " OR "

        return string

    # endregion

    # region VIEWS

    # VIEW FOR directors_movies_budget, directors_budget
    def directors_movies_budget_view(self):

        query = """
        CREATE OR REPLACE VIEW Movie_numOfActors_Director AS
            SELECT m.movie_ID, m.title, rm.num_of_actors, m.budget, mc.person_ID, p.first_name, p.last_name,
                p.picture_URL, m.poster_URL
            FROM Movies m, Person p, Movies_Crew mc, (
                          SELECT m.movie_ID, COUNT(*) as num_of_actors
                          FROM Movies m, Movies_Actors ma
                          WHERE m.movie_ID = ma.movie_ID
                          GROUP BY m.movie_ID
                          ) rm
            WHERE mc.role ="Director" AND mc.movie_ID = m.movie_ID
                AND m.movie_ID=rm.movie_ID AND mc.person_ID = p.person_ID
            """

        self.execute_sql(query)


    # VIEW FOR director_actor_coupling
    def director_actor_coupling_view(self):

        query = """
        CREATE OR REPLACE VIEW Director_Actor_Genre_NumOfMovies AS
            SELECT g.genre_ID, g.genre, COUNT(*) AS co_operations, p1.person_ID AS director_ID, p1.first_name AS director_first_name, p1.last_name AS director_last_name,
                p1.picture_URL AS director_pic,p2.person_ID AS actor_ID, p2.first_name AS actor_first_name, p2.last_name AS actor_last_name, p2.picture_URL AS actor_pic
            FROM Person p1, Person p2, Movies_Crew mc, Movies_Actors ma, Movies m, Movie_Genres mg, Genres g
            WHERE p1.person_ID=mc.person_ID AND p2.person_ID=ma.person_ID AND
                mc.role = "Director" AND mc.movie_ID=m.movie_ID AND ma.movie_ID=m.movie_ID
                AND m.movie_ID = mg.movie_ID AND mg.genre_ID = g.genre_ID
            GROUP BY g.genre_ID, g.genre, p1.person_ID, p1.first_name, p1.last_name, p2.person_ID, p2.first_name, p2.last_name
            """

        self.execute_sql(query)

    #endregion


    # region GETTERS

    def get_movies_ratings(self):
        query = f"""
            SELECT *, (ms.rotten_tomatoes+ ms.metacritic+ ms.imdb)/3 AS popularity
            FROM Movies m, Movie_Score ms, Rated r
            WHERE m.movie_ID = ms.movie_ID AND m.rated_ID = r.rated_ID
            ORDER BY popularity DESC
        """
        rows = self.execute_sql(query)
        return rows

    def get_movie_rating(self, m_id):
        query = f"""
            SELECT (ms.rotten_tomatoes+ ms.metacritic+ ms.imdb)/3 AS popularity
            FROM Movies m, Movie_Score ms, Rated r
            WHERE m.movie_ID = ms.movie_ID AND m.rated_ID = r.rated_ID AND m.movie_ID = {m_id}
        """
        rows = self.execute_sql(query)
        return rows

    def get_movie_genres(self, m_id):
        query = f"""
            SELECT GROUP_CONCAT(g.genre)
            FROM Movies m, Movie_Genres mg, Genres g
            WHERE m.movie_ID = mg.movie_ID AND mg.genre_ID = g.genre_ID AND m.movie_ID = {m_id}
            GROUP BY m.movie_ID
        """
        rows = self.execute_sql(query)
        return rows

    def get_movie_director(self, m_id):
        query = f"""
            SELECT p.*
            FROM Movies m, Movies_Crew mc, Person p
            WHERE m.movie_ID = mc.movie_ID AND mc.person_ID = p.person_ID AND m.movie_ID = {m_id} AND mc.role = "Director"
        """
        rows = self.execute_sql(query)[0][1:3]
        director_name = rows[0] + " " + rows[1]
        return director_name

    def get_movie_actors(self, m_id):
        query = f"""
            SELECT p.*
            FROM Movies m, Movies_Actors ma, Person p
            WHERE m.movie_ID = ma.movie_ID AND ma.person_ID = p.person_ID AND m.movie_ID = {m_id}
        """
        rows = self.execute_sql(query)
        actors = [act[1] + " " + act[2] for act in rows]
        return actors

    #endregion

