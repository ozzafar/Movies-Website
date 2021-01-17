import html

class IndexMovie:
    _color_num = 0

    def __init__(self, title, poster, categories_list, avg_rating, movie_id):
        self._movie_id = movie_id
        self._title = title
        self._poster = "https://image.tmdb.org/t/p/w300/" + poster
        self._categoryList = categories_list
        if avg_rating is None:
            avg_rating = -10
        self._rating = "%.1f" % round(avg_rating/10, 1)

    def get_html_body(self):
        colors = {0: "blue", 1: "yell", 2: "green", 3: "orange"}
        body = """
        <div class="movie-item">
            <div class="mv-img">
                <a href="#"><img src="""+self._poster+""" alt="" width="285" height="437"></a>
            </div>
            <div class="title-in">
	    		<div class="cate"> """

        for i in range(len(self._categoryList)):
            body += "<span class="+colors[IndexMovie._color_num]+">"+self._categoryList[i]+"</span>"
            IndexMovie._color_num = (self._color_num + 1) % len(colors)

        body += """
                </div>
                <h6><a href="/moviesingle?movie="""+str(self._movie_id)+""""">"""+self._title+"""</a></h6>
                <p><i class="ion-android-star"></i><span>"""+self._rating+"""</span> /10</p>
            </div>
        </div> """

        return html.unescape(body)

class CelebrityInfo:

    def __init__(self, first_name, last_name, job, poster, num_of_movies):
        self._first_name = first_name
        self._last_name = last_name
        self._poster = "https://image.tmdb.org/t/p/w300/" + poster
        self._job = job
        self._num_of_movies = num_of_movies

    def get_html_body(self):
        body = """
        <div class="ceb-item">
            <img src="""+self._poster+""" alt="" width="270" height="400">
            <div class="ceb-infor">
                <h2>"""+self._first_name+""" """+self._last_name+"""</h2>
                <span>"""+self._job+""", Participated in """+self._num_of_movies+""" films</span>
            </div>
        </div> """
        return html.unescape(body)

# class for movies_grid page
class MovieInfo:
    _color_num = 0

    def __init__(self, title, poster, categories_list, avg_rating, movie_id):
        self._movie_id = movie_id
        self._title = title
        self._poster = "https://image.tmdb.org/t/p/w300/" + poster
        self._categoryList = categories_list
        if avg_rating is None:
            avg_rating = -10
        self._rating = "%.1f" % round(avg_rating/10, 1)

    def get_html_body(self):
        colors = {0: "blue", 1: "yell", 2: "green", 3: "orange"}
        body = """
        <div class="movie-item">
            <div class="mv-img">
                <a href="#"><img src="""+self._poster+""" alt="" width="285" height="437"></a>
            </div>
            <div class="title-in">
	    		<div class="cate"> """

        for i in range(len(self._categoryList)):
            body += "<span class="+colors[IndexMovie._color_num]+">"+self._categoryList[i]+"</span>"
            IndexMovie._color_num = (self._color_num + 1) % len(colors)

        body += """
                </div>
                <h6><a href="/moviesingle?movie="""+str(self._movie_id)+""""">"""+self._title+"""</a></h6>
                <p><i class="ion-android-star"></i><span>"""+self._rating+"""</span> /10</p>
            </div>
        </div> """

        return html.unescape(body)