import mysql.connector
from mysql.connector import errorcode

MIN_YEAR = 1900
MAX_YEAR = 2020
ALL = "*"

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

    def execute_sql(self, sql, values=None):
        cursor = self.cnx.cursor()  # get the cursor
        if values is None:
            iterator = cursor.execute(sql)
            return iterator
        else:
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

    # ---------------- Queries ------------------
    def recommendations(self, min_len, max_len, start_year=MIN_YEAR, end_year=MAX_YEAR):
        pass
        # query = f"\
        # CREATE VIEW Relevant_Movies AS:\
        # SELECT m.movie_ID AS movie_ID, m.movie_name AS name, g.genre AS genre,\
        #     SUM(ms.rotten_tomatoes, ms.metacritic, ms.imdb) / 3 AS popularity \
        # FROM Movies m, Movie_Genres mg, Genres g, Movie_Score ms \
        # WHERE m.movie_ID = mg.movie_ID AND mg.genre_ID = g.genre_ID AND \
        #     EXTRACT(YEAR FROM m.released) BETWEEN {start_year} AND {end_year} \
        #     AND (EXTRACT(HOUR FROM m.run_time)*60+EXTRACT(MINUTE FROM m.run_time))\
        #         BETWEEN {min_len} AND {max_len} AND m.movie_ID = ms.movie_ID \
        #     \
        # SELECT rm_n.movie_ID, rm_n.title, rm_n.genre, rm_n.released, \
        #     rm_n.run_time, rm_n.popularity \
        # FROM( \
        #     SELECT rm.movie_ID, rm.title, rm.genre, rm.released, \
        #         rm.run_time, rm.popularity, ROW_NUMBER OVER(Partition BY rm.genre \
        #         ORDER BY rm.popularity DESC) AS popularity_rank \
        #     FROM Relevant_Movies AS rm \
        #     ) rm_n \
        # WHERE rm_n.popularity_rank <= 10 \
        # ORDERED BY rm_n.genre, rm_n.popularity"
        #
        # iterator = self.execute_sql(query)
        # return iterator


# If user doesn't specifies user_genre - return all categories. Same with years
    def popular_movies(self, user_genre=ALL, start_year=MIN_YEAR, end_year=MAX_YEAR):
        pass
        # query = f"\
        # SELECT M.title, SUM(ms.rotten_tomatoes, ms.metacritic, ms.imdb)/3 AS popularity \
        # FROM Movies m, Movies_Score ms, Movies_Genres mg, Genres g \
        # WHERE m.movie_ID = ms.movie_ID AND EXTRACT(YEAR FROM m.released) \
        # BETWEEN {start_year} AND {end_year} AND ms.movie_ID = mg.movie_ID \
        #     AND mg.genre_ID = g.genre_ID \
        #     AND g.genre = {user_genre} \
        # ORDER BY popularity"
        #
        # iterator = self.execute_sql(query)
        # return iterator

    def popular_actors(self, start_year=MIN_YEAR, end_year=MAX_YEAR, movie_score=0):
        pass
        # query = f"\
        # SELECT p.first_name, p.last_name, COUNT(*) AS amount_of_movies \
        # FROM Person p, Movies_Actors ma, Movie_Score ms \
        # WHERE EXTRACT(YEAR FROM m.released) BETWEEN {start_year} AND {end_year} \
        #     AND {movie_score} >= (ms.rotten_tomatoes +  ms.metacritic + ms.imdb)/3 \
        #     AND p.person_ID = ma.person_ID AND ma.movie_ID = ms.movie_ID \
        # GROUP BY ma.Person_ID \
        # ORDER BY amount_of_movies"
        #
        # iterator = self.execute_sql(query)
        # return iterator

    def director_actor_coupling(self, number_of_movies, user_genre=ALL):
        pass
        # query = f"\
        # SELECT p1.person_ID, p1.first_name, p1.last_name, p2.person_ID, p2.first_name, \
        #     p2.last_name, COUNT(*) as co-operations \
        # FROM Person p1, Person p2, Movies-Crew mc, Movies-Actors ma, Movies m,\
        #     Movies-Genres mg, Genres g \
        # WHERE p1.person_ID=mc.person_ID AND p2.person_ID=ma.person_ID AND \
        #     mc.role = \“Director\” AND mc.movie_ID=m.movie_ID AND ma.movie_ID=m.movie_ID \
        #     AND m.movie_ID = mg.movie_ID AND g.genre = {user_genre}\
        # GROUP BY p1.Person-ID, p1.First-name, p1.Last-name, p2.Person-ID, p2.First-\
        #     name, p2.Last-name\
        # HAVING co-operations > {number_of_movies}"
        #
        # iterator = self.execute_sql(query)
        # return iterator

    # user can ignore awards
    def countries_movies(self, movie_budget, movie_awards=0):
        pass
        # query = f" \
        # CREATE VIEW Countries_Movies AS: \
        #     SELECT pc.country, m.title, m.budget, m.awards \
        #     FROM Production_Countries pc, Movies_Countries mc, Movies m \
        #     WHERE pc.prod_country_ID = mc.prod_country_ID AND mc.movie_ID = m.movie_ID \
        #         AND m.budget >= {movie_budget} AND m.awards >= {movie_awards}\
        #     \
        # SELECT cm_n.country, cm_n.title, cm_n.budget, cm_n.awards \
        # FROM( \
        #     SELECT cm.country, cm.title, cm.budget, cm.awards, \
        #         ROW_NUMBER over(Partition BY cm.country \
        #         ORDER BY cm.budget, cm.awards DESC) AS ranked_budget \
        #     FROM Countries_Movies AS cm \
        #     ) cm_n \
        # WHERE cm_n.ranked_budget <= 10 # for each country return only 10 countries\
        # ORDER BY cm_n.country, cm_n.budget, cm_n.awards"
        #
        # iterator = self.execute_sql(query)
        # return iterator

    def directors_movies_budget(self, budget, num_of_directors=10, actors_number=1):
        pass
        # query = f"\
        # CREATE VIEW Relevant_Movies AS: \
        #     #(returns movies that have more than \“actors_number\” actors)\
        #     SELECT m.movie_ID, COUNT(*) as num_of_actors\
        #     FROM Movies m, Movies_Actors ma\
        #     WHERE m.movie_ID = ma.movie_ID\
        #     GROUP BY m.movie_ID\
        #     HAVING num_of_actors >= {actors_number} \
        #         \
        # CREATE VIEW Relevant_Directors AS: \
        #     #(returns top \“num_of_directors\” directors that produced movies with at least \“actors_number\” actors or more, and their total budget is at least \“budget\”) \
        #     SELECT mc.person_ID, SUM(m.budget) AS total_budget \
        #     FROM Movies_Crew mc, Relevant_Movies rm \
        #     WHERE mc.role =\”Director\” AND mc.movie_ID = m.movie_ID \
        #         AND m.movie_ID = rm.movie_ID \
        #     GROUP BY mc.person_ID \
        #     HAVING total_budget >= {budget} \
        #     LIMIT {num_of_directors} \
        #     \
        # SELECT p.person_ID, p.last_name, p.first_name, m.title, m.budget, rm.num_of_actors\
        # FROM Person p, Relevant_Directors rd \
        # WHERE p.pesron_ID = rd.person_ID AND p.person_ID = mc.person_ID \
        #     AND mc.movie_ID = rm.movie_ID \
        # ORDERED BY p.last_name, p.first_name"
        #
        # iterator = self.execute_sql(query)
        # return iterator

    # uses sub query of directors_movies_budget()
    # return Director-total_budget (total_budget is the total_budget of movies made by the director)
    def directors_budget(self, budget, num_of_directors=10, actors_number=1):
        pass
        # query = f"\
        # CREATE VIEW Relevant_Movies AS: \
        #     #(returns movies that have more than \“actors_number\” actors)\
        #     SELECT m.movie_ID, COUNT(*) as num_of_actors\
        #     FROM Movies m, Movies_Actors ma\
        #     WHERE m.movie_ID = ma.movie_ID\
        #     GROUP BY m.movie_ID\
        #     HAVING num_of_actors >= {actors_number} \
        #         \
        # #(returns top \“num_of_directors\” directors that produced movies with at least \“actors_number\” actors or more, and their total budget is at least \“budget\”) \
        # SELECT mc.person_ID, SUM(m.budget) AS total_budget \
        # FROM Movies_Crew mc, Relevant_Movies rm \
        # WHERE mc.role =\”Director\” AND mc.movie_ID = m.movie_ID \
        #     AND m.movie_ID = rm.movie_ID \
        # GROUP BY mc.person_ID \
        # HAVING total_budget >= {budget} \
        # LIMIT {num_of_directors}"

        # iterator = self.execute_sql(query)
        # return iterator

    def actors_movies_awards(self, num_of_actors, start_year=MIN_YEAR):
        pass
        # query = f"\
        # SELECT p.first_name, p.last_name, p.gender, COUNT(*) AS number_of_movies_played , \
        #         SUM(m.awards) AS total_awards\
        # FROM Person p, Movies_Actors ma, Movies m\
        # WHERE p.person_ID = ma.person_ID AND ma.movie_ID = m.movie_ID\
        #     AND EXTRACT(YEAR FROM m.released) > {start_year} \
        # GROUP BY p.person_ID, p.first_name, p.last_name, p.gender \
        # ORDER BY number_of_movies_played, total_awards\
        # LIMIT {num_of_actors}"
        #
        # iterator = self.execute_sql(query)
        # return iterator

    # ------ Full-Text Queries --------

    def movies_with_string_in_name(self, string_to_search, sub_string=False):
        pass
        # if sub_string:
        #     string_to_search = string_to_search + "*"
        #
        # query = f"\
        # SELECT m.title, r.rated, m.released, m.run_time, m.plot, m.awards, m.budget, m.revenue \
        # FROM Movies m, Rated r \
        # WHERE m.rated_ID = r.rated_ID AND Match(title) AGAINST({string_to_search} IN BOOLEAN MODE)"
        #
        # iterator = self.execute_sql(query)
        # return iterator

    def movies_with_string_in_plot(self, string_to_search, sub_string=False):
        pass
        # if sub_string:
        #     string_to_search = string_to_search + "*"
        #
        # query = f"\
        # SELECT m.title, r.rated, m.released, m.run_time, m.plot, m.awards, m.budget, m.revenue\
        # FROM Movies m, Rated r\
        # WHERE m.rated_ID = r.rated_ID AND Match(m.plot) AGAINST({string_to_search} IN BOOLEAN MODE)"
        #
        # iterator = self.execute_sql(query)
        # return iterator

    def movies_actors_with_string_in_name(self, string_to_search, sub_string=False):
        pass
        # if sub_string:
        #     string_to_search = string_to_search + "*"
        #
        # query = f"\
        # SELECT m.movie_ID, m.title, COUNT(*) as num_of_actors\
        # FROM Movies m, Movies_Actors ma, Person p\
        # WHERE m.movie_ID = ma.movie_ID AND p.person_ID = ma.person_ID\
        #     AND Match(p.first_name, p.last_name) AGAINST({string_to_search} IN BOOLEAN MODE) \
        # GROUP BY m.movie_ID, m.title \
        # ORDER BY num_of_actors"
        #
        # iterator = self.execute_sql(query)
        # return iterator
