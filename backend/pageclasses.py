import html

class IndexMovie:
    _color_num = 0

    def __init__(self, title, poster, categories_list, avg_rating):
        self._title = title
        self._poster = "https://image.tmdb.org/t/p/w300/" + poster
        self._categoryList = categories_list
        self._rating = avg_rating

    def get_html_body(self):
        colors = {0: "blue", 1: "yell", 2: "green", 3: "orange"}
        body = """
        <div class="movie-item">
            <div class="mv-img">
                <a href="#"><img src="""+self._poster+""" alt="" width="285" height="437"></a>
            </div>
            <div class="title-in">
	    		<div class="cate"> """  # TODO change <a href="#"> to go to its page

        for i in range(len(self._categoryList)):
            body += "<span class="+colors[IndexMovie._color_num]+">"+self._categoryList[i]+"</span>"
            IndexMovie._color_num = (self._color_num + 1) % len(colors)

        body = """
                </div>
                <h6><a href="#">"""+self._title+"""</a></h6>
                <p><i class="ion-android-star"></i><span>"""+str(self._rating/10)+"""</span> /10</p>
            </div>
        </div> """  # TODO change <a href="#"> to go to its page

        return html.unescape(body)