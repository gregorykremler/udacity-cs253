# Udacity CS253
# https://www.udacity.com/course/cs253

"""
Toy application suite covering core web development concepts built on
Google App Engine for Udacity CS253: Web Application Engineering.
"""


import webapp2
from handlers import BaseHandler
from birthday import Birthday, Thanks
from rot13 import Rot13
from signup import QuerySignup, QueryWelcome
from ascii import Ascii
from blog import Blog, NewPost, Permalink
from visits import Visits
from signup import dbSignup, dbWelcome
from login import Login
from logout import Logout
from mapscii import Mapscii
from cachedscii import Cachedscii
from cachedblog import CachedBlog, NewCachedPost, CachedPermalink, BlogFlush


class MainPage(BaseHandler):
    def get(self):
        self.render('index.html')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/birthday', Birthday),
                               ('/thanks', Thanks),
                               ('/rot13', Rot13),
                               ('/signup', QuerySignup),
                               ('/welcome', QueryWelcome),
                               ('/ascii', Ascii),
                               ('/blog/?(?:\.json)?', Blog),
                               ('/blog/newpost', NewPost),
                               ('/blog/([0-9]+)(?:\.json)?', Permalink),
                               ('/visits', Visits),
                               ('/db-signup', dbSignup),
                               ('/db-welcome', dbWelcome),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/mapscii', Mapscii),
                               ('/cachedscii', Cachedscii),
                               ('/cached-blog?(?:\.json)?', CachedBlog),
                               ('/cached-blog/newpost', NewCachedPost),
                               ('/cached-blog/([0-9]+)(?:\.json)?',
                                CachedPermalink),
                               ('/cached-blog/flush', BlogFlush)])
