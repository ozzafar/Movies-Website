from DBbackend import DBbackend
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    filename = ''
    css = ''
    body = ''
    js1 = ''
    js2 = ''
    genres = request.args.get('genre')
    if is_valid_genre(genres):
        movie_length = request.args.get('movieLength')
        if is_valid_movie_length(movie_length): # genres != None and (is list and len(genres) == 2
            release = request.args.get('release')
            if release == 'pre' or release == 'old' or release == 'new' or release == 'all':
                return render_template('index.html')
            else:
                filename = 'slider2'
                css = '        .container {\
            width: 500px !important;\
            left: 50% !important;\
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
    var categories = [];\
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
    return render_template('intro.html', filename=filename, css=css, body=body, js1=js1, js2=js2)


def is_valid_movie_length(movie_length):
    if movie_length[0] >= 0 and movie_length[1] <= 240:
        return True
    return False


def is_valid_genre(genre):  # genres != None and ((is list and len(genres) > 0) or (is string and in DB))
    if genre is not None:
        if (type(genre) is list and len(genre) > 0) or (isinstance(genre, str) and genre in list_of_genres_db()):
            return True
    return False


def list_of_genres_db():
    db = DBbackend()
    sql = 'SELECT genre FROM Genres'
    res = db.execute_sql(sql)
    genres = [g[0] for g in res]
    db.close()
    return genres


if __name__ == '__main__':
    app.run(port="40004", debug=False)

