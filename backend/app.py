import math
from DBbackend import DBbackend
import html
import AuxiliaryFuncs
from config import *
from flask import Flask, render_template, request

app = Flask(__name__)

db = DBbackend()

def create_movie_body(page):
    is_search = False

    body = ""
    search_query = ""
    movies=[]

    # search fields:
    if 'submit' in request.args.keys():
        is_submitted = request.args.get('submit')
        if type(is_submitted) is str:
            if is_submitted == 'submit':
                exact_match = request.args.get('exact_match')
                movie_title = request.args.get('movie_title')
                genres = request.args.get('genres')
                minimum_rating = request.args.get('minimum_rating')
                from_year = request.args.get('from_year')
                to_year = request.args.get('to_year')
                is_search = True
                search_query = f" - {exact_match} \"{movie_title}\", Genres: {genres},  Minimum rating: {minimum_rating}, From {from_year} to {to_year}"
    if is_search:
        movies = db.movies_with_string_in_name_query(movie_title, int(minimum_rating)*10,
                    genres.split(","), int(from_year), int(to_year), sub_string=(exact_match == "contains"))
        #print('num of movies1: ' + str(len(movies)))
        poster_url_index = 4
        id_index = 0
        name_index = 1
        rating_index = 3
    else:
        movies = db.get_movies_ratings()
        #print('num of movies2: '+str(len(movies)))
        poster_url_index = 9
        id_index = 0
        name_index = 1
        rating_index = 18

    # pagination
    num_of_res = len(movies)
    first_result = (NUM_OF_RESULTS_PER_PAGE_2 * (page - 1))
    last_result = NUM_OF_RESULTS_PER_PAGE_2 * page
    movies = movies[first_result:min(len(movies), last_result)]

    for i in range(0,len(movies)):

        if movies[i][id_index] is None or movies[i][name_index] is None or movies[i][rating_index] is None:
            continue
        poster_url = movies[i][poster_url_index]
        if movies[i][rating_index] is None:
            continue
        if poster_url != None:
            poster_url_full = "https://image.tmdb.org/t/p/w1280" + movies[i][poster_url_index]
        else:
            poster_url_full = "/static/images/no_photo_availble.png"
        id = str(movies[i][id_index])
        name = movies[i][name_index]
        rating = str(movies[i][rating_index] / 10)[:3]
        body += (f"""
                <div class="movie-item-style-2 movie-item-style-1">
                    <img src={poster_url_full} alt="">
                    <div class="hvr-inner">
                        <a  href=moviesingle?movie={id}> Read more <i class="ion-android-arrow-dropright"></i> </a>
                    </div>
                    <div class="mv-item-infor">
                        <h6><a href=moviesingle?movie={id}> {name} </a></h6>
                        <p class="rate"><i class="ion-android-star"></i><span>{rating}</span> /10</p>
                    </div>
                </div>""")
    return body, num_of_res, search_query


@app.route('/moviesingle', methods=['GET'])
def moviesingle():
    movie_id = request.args.get('movie')
    movie = db.get_movie(movie_id)[0]

    plot = movie[5]
    if plot is None:
        plot = "Sorry, plot is not available"

    if movie[3] is None:
        year = "Sorry, year is not available"
    else:
        if movie[3].year is None:
            year = "Sorry, year is not available"
        else:
            year = movie[3].year

    name = movie[1]
    if name is None:
        name = "Sorry, name is not available"

    trailer = movie[10]
    if trailer is not None:
        trailer = "https://www.youtube.com/watch?v=" + movie[10]

    if movie[9] is None:
        poster = "/static/images/no_photo_availble.png"
    else:
        poster = "https://image.tmdb.org/t/p/w1280" + movie[9]

    if movie[3] is None:
        date = "Sorry, date is not available"
    else:
        date = str(movie[3])

    if movie[4] is None:
        runtime = "Sorry, runtime is not available"
    else:
        runtime = str(movie[4])

    rating = db.get_movie_rating(movie_id)
    if len(rating) == 0:
        rating = "Sorry, rating is not available"
    else:
        rating = str(rating[0][0]/10)[:3] + " /10"

    director = db.get_movie_director(movie_id)
    if director is None:
        director = "Sorry, director's name is not available"

    actors = db.get_movie_actors(movie_id)
    if len(actors) == 0:
        actors.append("Sorry, actors names is not available")

    genres_db = db.get_movie_genres(movie_id)
    if len(genres_db)==0:
        genres = "Sorry, genres are not available"
    else:
        genres_db = (genres_db[0])[0].split(',')
        genres = ""
        for i in range(len(genres_db) - 1):
            genres = genres + genres_db[i] + ", "
        genres += genres_db[-1]

    return render_template('moviesingle.html', name=name, year=year, runtime=runtime, plot=plot,
                           date=date, poster=poster, trailer=trailer,
                           genres=genres, director=director, actors=actors, rating=rating)


@app.route('/moviegrid', methods=['GET', 'POST'])
def moviegrid():
    # pagination
    page = request.args.get('page')
    if type(page) is str:
        page = int(page)
    else:
        page = 1

    body, num_of_res, search_query = create_movie_body(page)

    list_of_pages = range(1, math.ceil(num_of_res / NUM_OF_RESULTS_PER_PAGE_2) + 1)

    return render_template('moviegrid.html', body=body, genres=list_of_genres_db(), num_of_res=num_of_res,
                           search_query=search_query, page_no=page, num_of_pages=len(list_of_pages),
                           pages=list_of_pages)


@app.route('/facts', methods=['GET', 'POST'])
def fun_facts():
    fact = request.args.get('fact')
    init = [" selected", ""]
    couples = ["", " display:none;"]
    popular_directors = ["", " display:none;"]
    countries_movies = ["", " display:none;"]
    actors_awards = ["", " display:none;"]
    movies_with_actors_by_name = ["", " display:none;"]
    selected = 0
    display = 1
    if type(fact) is str:
        is_form_sent = False
        is_submitted = request.args.get('submit')
        res = []

        if fact == 'couples':
            search_query = ''
            if type(is_submitted) is str:
                if is_submitted == 'submit':
                    is_form_sent = True
                    num_of_common_movies = int(request.args.get('number_of_common_movies'))
                    genres = str(request.args.get('genres'))
                    genres_lst = genres.split(',')
                    genres_lst = [x.strip() for x in genres_lst]
                    search_query = f" - Number of common movies: {num_of_common_movies}, Genres: {genres}"
                    res = db.director_actor_coupling_query(num_of_common_movies, genres_lst)
            init = ["", " display:none;"]
            couples = [" selected", ""]
            popular_directors = ["", " display:none;"]
            countries_movies = ["", " display:none;"]
            actors_awards = ["", " display:none;"]
            movies_with_actors_by_name = ["", " display:none;"]
            # pagination
            num_of_res = len(res)
            page = request.args.get('page')
            if type(page) is str:
                page = int(page)
            else:
                page = 1
            list_of_pages = range(1, math.ceil(num_of_res / NUM_OF_RESULTS_PER_PAGE_2) + 1)
            first_result = (NUM_OF_RESULTS_PER_PAGE_2 * (page - 1))
            last_result = NUM_OF_RESULTS_PER_PAGE_2 * page
            res = res[first_result:min(num_of_res, last_result)]
            return render_template('facts_couples.html', selected=selected, display=display, init=init, couples=couples,
                                   popular_directors=popular_directors, countries_movies=countries_movies,
                                   actors_awards=actors_awards, movies_with_actors_by_name=movies_with_actors_by_name,
                                   is_form_sent=is_form_sent, genres=list_of_genres_db(), res=res,
                                   director_pic=3, director_first_name=1, director_last_name=2,
                                   actor_pic=7, actor_first_name=5, actor_last_name=6, co_operations=8, user_genres=9,
                                   search_query=search_query, page_no=page, num_of_pages=len(list_of_pages),
                                   pages=list_of_pages, num_of_res=num_of_res, fact=fact)
        elif fact == 'popular_directors':
            # TODO add <br> every 18 chars in long movie/people names
            search_query = ""
            if type(is_submitted) is str:
                if is_submitted == 'submit':
                    is_form_sent = True
                    budget = request.form.get('budget')
                    if budget == '':
                        budget = '0'
                    budget = int(budget)
                    num_of_actors = request.form.get('num_of_actors')
                    if num_of_actors == '':
                        num_of_actors = '0'
                    num_of_actors = int(num_of_actors)
                    search_query = f" - Budget: {budget}, Number of production companies: {num_of_actors}"
                    res = db.directors_movies_budget_query(budget, num_of_actors)
# director_picture director_first_name director_last_name movie_ID movie_poster title num_of_actors total_budget
            init = ["", " display:none;"]
            couples = ["", " display:none;"]
            popular_directors = [" selected", ""]
            countries_movies = ["", " display:none;"]
            actors_awards = ["", " display:none;"]
            movies_with_actors_by_name = ["", " display:none;"]
            return render_template('facts_popular_directors.html', selected=selected, display=display, init=init,
                                   couples=couples, popular_directors=popular_directors,
                                   countries_movies=countries_movies, actors_awards=actors_awards,
                                   movies_with_actors_by_name=movies_with_actors_by_name, is_form_sent=is_form_sent,
                                   res=res, person_ID=0, director_first_name=1, director_last_name=2,
                                   director_picture_URL=3, movie_ID = 4, title=5, num_of_actors=6, budget=7, total_budget=8, movie_poster=9,
                                   movie_index=10, movie_max_index=11, search_query=search_query)
        elif fact == 'countries_movies':
            search_query = ""
            if type(is_submitted) is str:
                if is_submitted == 'submit':
                    is_form_sent = True
                    budget = request.form.get('budget')
                    if budget == '':
                        budget = '0'
                    budget = int(budget)
                    num_of_awards = request.form.get('num_of_awards')
                    if num_of_awards == '':
                        num_of_awards = '0'
                    num_of_awards = int(num_of_awards)
                    search_query = f" - Budget: {budget}, Number of awards: {num_of_awards}"
                    res = db.countries_movies_query(budget, num_of_awards)
            init = ["", " display:none;"]
            couples = ["", " display:none;"]
            popular_directors = ["", " display:none;"]
            countries_movies = [" selected", ""]
            actors_awards = ["", " display:none;"]
            movies_with_actors_by_name = ["", " display:none;"]
            return render_template('facts_countries_movies.html', selected=selected, display=display, init=init,
                                   couples=couples, popular_directors=popular_directors,
                                   countries_movies=countries_movies, actors_awards=actors_awards,
                                   movies_with_actors_by_name=movies_with_actors_by_name, is_form_sent=is_form_sent,
                                   res=res, movie_poster=5, movie_ID=1, title=2, country=0, budget=3, awards=4,
                                   search_query=search_query)
        elif fact == 'actors_awards':
            search_query = ""
            if type(is_submitted) is str:
                if is_submitted == 'submit':
                    is_form_sent = True
                    start_year = request.form.get('start_year')
                    search_query = f" - From {start_year}"
                    start_year = int(start_year)
                    res = db.actors_movies_awards_query(start_year)
            init = ["", " display:none;"]
            couples = ["", " display:none;"]
            popular_directors = ["", " display:none;"]
            countries_movies = ["", " display:none;"]
            actors_awards = [" selected", ""]
            movies_with_actors_by_name = ["", " display:none;"]
            return render_template('facts_actors_awards.html', selected=selected, display=display, init=init,
                                   couples=couples, popular_directors=popular_directors,
                                   countries_movies=countries_movies, actors_awards=actors_awards,
                                   movies_with_actors_by_name=movies_with_actors_by_name, is_form_sent=is_form_sent,
                                   res=res, first_name=1, last_name=2, movies_played=3,
                                   total_awards=4, picture_URL=5, search_query=search_query)
        elif fact == 'movies_with_actors_by_name':
            search_query = ""
            if type(is_submitted) is str:
                if is_submitted == 'submit':
                    is_form_sent = True
                    exact_match = request.form.get('exact_match')
                    string_to_search = request.form.get('string_to_search')
                    res = db.movies_actors_with_string_in_name_query(string_to_search, exact_match == "contains")
                    search_query = f" - {exact_match} \"{string_to_search}\""
            init = ["", " display:none;"]
            couples = ["", " display:none;"]
            popular_directors = ["", " display:none;"]
            countries_movies = ["", " display:none;"]
            actors_awards = ["", " display:none;"]
            movies_with_actors_by_name = [" selected", ""]
            return render_template('movies_with_actors_by_name.html', selected=selected, display=display, init=init,
                                   couples=couples, popular_directors=popular_directors,
                                   countries_movies=countries_movies, actors_awards=actors_awards,
                                   movies_with_actors_by_name=movies_with_actors_by_name, is_form_sent=is_form_sent,
                                   res=res, id = 0, title=1, num_of_actors=2, actors_string=3, poster_URL=4,
                                   search_query=search_query)

    return render_template('facts.html', selected=selected, display=display, init=init,
                           couples=couples, popular_directors=popular_directors,
                           countries_movies=countries_movies, actors_awards=actors_awards,
                           movies_with_actors_by_name=movies_with_actors_by_name)


@app.route('/celebritygrid', methods=['GET', 'POST'])
def celebritygrid():


    # form
    is_submitted = request.args.get('submit')
    res = []

    user_search = ''
    if type(is_submitted) is str:
        if is_submitted == 'submit': # TODO delete this if
            minimum_rating = request.args.get('minimum_rating')
            start_year = request.args.get('from_year')
            end_year = request.args.get('to_year')
            user_search = f", Minimum rating {minimum_rating} from {start_year} to {end_year}"
            res = db.popular_actors_query(int(minimum_rating)*10, int(start_year), int(end_year))
    else:
        res = db.popular_actors_query(0, 1500, 3000)

    # pagination
    num_of_res = len(res)
    page = request.args.get('page')
    if type(page) is str:
        page = int(page)
    else:
        page = 1
    list_of_pages = range(1, math.ceil(len(res)/NUM_OF_RESULTS_PER_PAGE)+1)
    first_result = (NUM_OF_RESULTS_PER_PAGE*(page-1))
    last_result = NUM_OF_RESULTS_PER_PAGE*page
    res = res[first_result:min(len(res), last_result)]

    return render_template('celebritygrid.html', res=res, user_search=user_search,
                           first_name=1, last_name=2, num_of_movies=4, picture_URL=5,
                           page_no=page, num_of_pages=len(list_of_pages), pages=list_of_pages, num_of_res=num_of_res)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    filename = ''
    css = ''
    body = ''
    js1 = ''
    js2 = ''
    bodyMor = ""
    genres = request.args.get('category')
    if is_valid_genre(genres):
        movie_length = request.args.get('movieLength')
        if is_valid_movie_length(movie_length):  # genres != None and (is list and len(genres) == 2
            release = request.args.get('release')
            if release == 'pre' or release == 'old' or release == 'new' or release == 'all':
                movies_info = AuxiliaryFuncs.query_to_index_movie(db, genres, movie_length, release)
                num_of_movies = min(20, len(movies_info))

                bodyMor = "<div class=\"slick-multiItemSlider\">"
                for movie_index in range(num_of_movies):
                    bodyMor += movies_info[movie_index].get_html_body()
                bodyMor += "</div>"

                if len(movies_info) == 0:
                    bodyMor = """
                    <p style="font-size: 20px; background-color: white; border-radius: 20px; padding: 20px; color: black; font-weight: bold;">
                    Found 0 movies
                    <br>
                    <a href="/">Click here to change your preferences</a></p>"""
                return render_template('index.html', body=bodyMor)
            else:
                filename = 'slider2'
                css = '        .container {\
            width: 500px !important;\
            left: 50% !important;\
            position: absolute;\
                top: 25%;\
                z-index: 2;\
                -webkit-animation: fadein 2s;\
                -moz-animation: fadein 2s;\
                -ms-animation: fadein 2s;\
                -o-animation: fadein 2s;\
                animation: fadein 2s;\
        }\
                .container-wrapper {\
            position: relative;\
            left: -50%;\
        }\
\
        .button {\
            font-weight: bold;\
            font-family: Dosis, sans-serif;\
            background-color: #008CBA;\
            padding: 16px 32px;\
            text-align: center;\
            text-decoration: none;\
            display: inline-block;\
            font-size: 16px;\
            margin: 4px 0px;\
            transition-duration: 0.4s;\
            cursor: pointer;\
            float:left;\
            color: black;\
            border: 2px solid #008CBA;\
            border-right: 0px;\
        }\
\
        .button:hover {\
            background-color: #008CBA;\
            color: white;\
        }\
\
        .button-first {\
            border-left: 2px solid #008CBA;\
            border-bottom-left-radius: 15px;\
            border-top-left-radius: 15px;\
        }\
\
        .button-last {\
            border-right: 2px solid #008CBA;\
            border-bottom-right-radius: 15px;\
            border-top-right-radius: 15px;\
        }\
\
        button:focus {outline:0;}\
\
        .selected {\
            background-color: #008CBA;\
            color: white;\
        }'
                body = '<h2 style="color:white; text-align:center; display:block">Release year:</h2>\
<div class="container">\
    <div class="container-wrapper">\
    <button class="button button-first" id="pre">pre 80\'s</button>\
    <button class="button" id="old">80\'s-90\'s</button>\
    <button class="button" id="new">2000-today</button>\
    <button class="button button-last" id="all">all</button>\
    </div>\
</div>'
                js2 = '<script src="https://code.jquery.com/jquery-3.5.0.js"></script>\
<script type="text/javascript">\
\
    $( "button" ).click(function() {\
        $( "button" ).removeClass( "selected" );\
        $(this).addClass( "selected" );\
    });\
\
    document.getElementById(\'findButton\').onclick = function () {\
        if (document.getElementsByClassName("selected").length > 0) {\
            var queryString = window.location.search;\
            if (queryString == "") queryString = "?";\
            var elementId = document.getElementsByClassName("selected")[0].id;\
            queryString += "&release=" + elementId;\
            location.href = "index" + queryString;\
        }\
        else {\
            alert("You must choose release year");\
        }\
    };\
</script>'
        else:
            filename = 'slider'
            css = '        @keyframes fadein {\
            from { opacity: 0; }\
            to   { opacity: 1; }\
        }\
\
        /* Firefox < 16 */\
        @-moz-keyframes fadein {\
            from { opacity: 0; }\
            to   { opacity: 1; }\
        }\
\
        /* Safari, Chrome and Opera > 12.1 */\
        @-webkit-keyframes fadein {\
            from { opacity: 0; }\
            to   { opacity: 1; }\
        }\
\
        /* Internet Explorer */\
        @-ms-keyframes fadein {\
            from { opacity: 0; }\
            to   { opacity: 1; }\
        }\
\
        /* Opera < 12.1 */\
        @-o-keyframes fadein {\
            from { opacity: 0; }\
            to   { opacity: 1; }\
        }\
        h2{\
            position: absolute;\
            left: 45%;\
            top: 35%;\
            z-index: 2;\
            -webkit-animation: fadein 2s; /* Safari, Chrome and Opera > 12.1 */\
            -moz-animation: fadein 2s; /* Firefox < 16 */\
            -ms-animation: fadein 2s; /* Internet Explorer */\
            -o-animation: fadein 2s; /* Opera < 12.1 */\
            animation: fadein 2s;\
        }\
\
        .container {\
            position: absolute;\
            left: 40%;\
            top: 25%;\
            z-index: 2;\
            -webkit-animation: fadein 2s; /* Safari, Chrome and Opera > 12.1 */\
            -moz-animation: fadein 2s; /* Firefox < 16 */\
            -ms-animation: fadein 2s; /* Internet Explorer */\
            -o-animation: fadein 2s; /* Opera < 12.1 */\
            animation: fadein 2s;\
        }'
            body = '<h2 style="color:white; text-align:center; display:block">Movie length:</h2>\
<div class="container">\
    <div class="slider">\
        <div class="track"></div>\
    </div>\
    <div class="output o0"> </div>\
    <div class="thumb t0"></div>\
\
    <div class="output o1"> </div>\
    <div class="thumb t1"></div>\
</div>'
            js2 = '<script type="text/javascript">\
    document.getElementById(\'findButton\').onclick = function () {\
        if (typeof roundedLength !== \'undefined\') {\
            var queryString = window.location.search;\
            if (queryString == "") queryString = "?";\
            queryString += "&movieLength="+roundedLength[0]+","+roundedLength[1];\
            location.href = "index"+queryString;\
        }\
    };\
</script>'
    else:
        filename = 'bubbles'
        body = '<div id="bubbles"></div>'
        js1 = '<script type="text/javascript">\
    var categories = [];' + get_js_genres_list() + '\
</script>'
        js2 = '<script type="text/javascript">\
    document.getElementById("findButton").onclick = function () {\
        if (categories.length>0) {\
            let queryString = "?category=";\
            for (let i = 0; i < categories.length; i++) {\
                queryString += categories[i];\
                if (i < categories.length-1) {\
                    queryString += ","\
                }\
            }\
            location.href = "index" + queryString;\
        } else {\
            alert("You must choose at least 1 category");\
        }\
    };\
</script>'

    css = html.unescape(css)
    body = html.unescape(body)
    js1 = html.unescape(js1)
    js2 = html.unescape(js2)
    csspath = 'static/css/' + filename + '.css'
    jspath = 'static/js/' + filename + '.js'
    return render_template('intro.html', csspath=csspath, css=css, body=body, jspath=jspath, js1=js1, js2=js2)


def is_valid_movie_length(movie_length):
    if type(movie_length) is str:
        movie_length_list = movie_length.split(',')
        if len(movie_length_list) == 2:
            if int(movie_length_list[0]) >= 0 and int(movie_length_list[1]) <= 210:
                return True
    return False


def is_valid_genre(genre):  # genres != None and ((is list and len(genres) > 0) or (is string and in DB))
    if type(genre) is str:
        genre_list = genre.split(',')
        if len(genre_list) > 0:
            all_in_db = True
            genres_db = list_of_genres_db()
            for g in genre_list:
                if g not in genres_db:
                    all_in_db = False
                    break
            return all_in_db
    return False


def list_of_genres_db():
    db = DBbackend()
    sql = 'SELECT genre FROM Genres'
    res = db.execute_sql(sql)
    genres = [g[0] for g in res]
    db.close()
    return genres


def get_js_genres_list():
    string = '\
    var nodes = new vis.DataSet(['
    for g in list_of_genres_db():
        string += '{label: "' + g + '"},'
    string += ']);\
'
    return string


if __name__ == '__main__':
    host = LOCALHOST
    if REMOTE:
        host = WEBSERVER
    app.run(port=PORT, debug=DEBUG, host=host)
