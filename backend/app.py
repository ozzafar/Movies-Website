from DBbackend import DBbackend
import html
import auxiliaryFuncs
from config import *
from flask import Flask, render_template, request

from pageclasses import IndexMovie

app = Flask(__name__)

db = DBbackend()

def create_body():

    movies = db.get_movies()
    body = ""
    page = int(request.args.get('page'))
    for i in range(20 * (page - 1), 20 * page):
        poster_url = movies[i][9]
        if poster_url != None:
            poster_url_full = "https://image.tmdb.org/t/p/w1280" + movies[i][9]
            id = str(movies[i][0])
            name = movies[i][1]
            body += ("""
            		<div class="movie-item-style-2 movie-item-style-1">
						<img src= """ + poster_url_full + """ alt="">
						<div class="hvr-inner">
							<a  href="moviesingle.html"> Read more <i class="ion-android-arrow-dropright"></i> </a>
						</div>
						<div class="mv-item-infor">
							<h6><a """ + "href=moviesingle?movie=" + id + ">" + name + """ </a></h6>
							<p class="rate"><i class="ion-android-star"></i><span>8.1</span> /10</p>
						</div>
					</div>""")
    return body


@app.route('/moviesingle', methods=['GET'])
def moviesingle():
    movie_id=request.args.get('movie')
    db = DBbackend()
    movie = db.get_movie(movie_id)[0]
    return render_template('/moviesingle.html', name=movie[1],year=movie[3].year,runtime=str(movie[4]),plot=movie[5],date=str(movie[3]),poster="https://image.tmdb.org/t/p/w1280"+movie[9])


@app.route('/moviegrid', methods=['GET'])
def moviegrid():
    body = create_body()
    return render_template('/moviegrid.html', body=body)

@app.route('/celebritygrid', methods=['GET'])
def celebritygrid():
    body = ""


    return render_template('/moviegrid.html', body=body)


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
        if is_valid_movie_length(movie_length): # genres != None and (is list and len(genres) == 2
            release = request.args.get('release')
            if release == 'pre' or release == 'old' or release == 'new' or release == 'all':
                movies_info = auxiliaryFuncs.query_to_index_movie(db, genres, movie_length, release)
                num_of_movies = min(11, len(movies_info))
                for movie_index in range(num_of_movies):
                    bodyMor += movies_info[movie_index].get_html_body()
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
    var categories = [];'+get_js_genres_list()+'\
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
    csspath = 'static/css/'+filename+'.css'
    jspath = 'static/js/'+filename+'.js'
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
        string += '{label: "'+g+'"},'
    string += ']);\
'
    return string


if __name__ == '__main__':
    host = LOCALHOST
    if REMOTE:
        host = WEBSERVER
    app.run(port=PORT, debug=DEBUG, host=host)
