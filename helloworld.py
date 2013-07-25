import os
import webapp2
import jinja2
import urllib2
import logging
from xml.dom import minidom
import json
import validations as v
from datetime import datetime, timedelta
from google.appengine.ext import db
from google.appengine.api import memcache


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = ('application/json; '
                                                 'charset-UTF-8')
        self.write(json_txt)

    def set_secure_cookie(self, name, val):
        cookie_val = v.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and v.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    # Override __init__ to check for user cookie on each request
    # If request URL ends with .json set 'json' format, else 'html'
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        user_id = self.read_secure_cookie('user_id')
        self.user = user_id and User.by_id(int(user_id))

        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'


class MainPage(BaseHandler):
    def get(self):
        self.write('Hello, Udacity!')


class Birthday(BaseHandler):
    def render_bday(self, month="", day="", year="", error=""):
        self.render('birthday-form.html', month=month, day=day, year=year,
                    error=error)

    def get(self):
        self.render_bday()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = v.valid_month(user_month)
        day = v.valid_day(user_day)
        year = v.valid_year(user_year)

        if not (month and day and year):
            error = "That doesn't look valid to me, friend."
            self.render_bday(user_month, user_day, user_year, error)
        else:
            self.redirect('/thanks')


class Thanks(BaseHandler):
    def get(self):
        self.write("Thanks! That's a totally valid day!")


class Rot13(BaseHandler):
    def render_rot13(self, text=""):
        self.render('rot13-form.html', text=text)

    def get(self):
        self.render_rot13()

    def post(self):
        text = v.rot13(self.request.get('text'))
        self.render_rot13(text)


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, user_id):
        return cls.get_by_id(user_id)

    @classmethod
    def by_name(cls, username):
        user = db.GqlQuery("SELECT * FROM User "
                           "WHERE name = :name ", name=username).get()
        return user

    @classmethod
    def register(cls, username, password, email=None):
        pw_hash = v.make_pw_hash(username, password)
        return cls(name=username, pw_hash=pw_hash, email=email)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.by_name(username)
        if user and v.valid_pw_hash(username, password, user.pw_hash):
            return user


class Signup(BaseHandler):
    def render_signup(self, username="", error_username="",
                      password="", error_password="",
                      verify="", error_verify="",
                      email="", error_email=""):
        self.render('signup-form.html', username=username,
                    error_username=error_username, password=password,
                    error_password=error_password, verify=verify,
                    error_verify=error_verify, email=email,
                    error_email=error_email)

    def get(self):
        self.render_signup()

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not v.valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not v.valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not v.valid_email(self.email):
            params['error_email'] = "That's not a valid e-mail."
            have_error = True

        if have_error:
            self.render_signup(**params)
        else:
            self.welcome()

    def welcome(self, *a, **kw):
        raise NotImplementedError


class ParamSignup(Signup):
    def welcome(self):
        self.redirect('/welcome?username=' + self.username)


class CookieSignup(Signup):
    def welcome(self):
        user = User.by_name(self.username)

        # Make sure the user doesn't already exist
        if user:
            error_username = "That user already exists."
            self.render_signup(username=self.username,
                               error_username=error_username,
                               email=self.email)
        else:
            user = User.register(self.username, self.password, self.email)
            user.put()

            self.login(user)
            self.redirect('/cookie-welcome')


class Login(BaseHandler):
    def render_login(self, username="", password="", error=""):
        self.render('login-form.html', username=username, password=password,
                    error=error)

    def get(self):
        self.render_login()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        # Authenticate pw_hash for this username
        user = User.authenticate(username, password)
        if user:
            self.login(user)
            self.redirect('/cookie-welcome')
        else:
            error = "Invalid login"
            self.render_login(username=username, error=error)


class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/cookie-signup')


class CookieWelcome(BaseHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/cookie-signup')


class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if v.valid_username(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('/signup')


IP_URL = "http://api.hostip.info/?ip="


def get_coords(ip):
    url = IP_URL + ip
    content = None

    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return

    if content:
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)


GMAPS_URL = ("http://maps.googleapis.com/maps/api/staticmap?"
             "size=380x263&sensor=false&")


def gmaps_img(points):
    markers = '&'.join('markers=%s,%s' % (p.lat, p.lon) for p in points)
    return GMAPS_URL + markers


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    coords = db.GeoPtProperty()
    created = db.DateTimeProperty(auto_now_add=True)


def top_arts(update=False):
    key = 'top'
    arts = memcache.get(key)

    if update or arts is None:
        logging.error("DB QUERY")
        arts = db.GqlQuery("SELECT * FROM Art "
                           "ORDER BY created DESC "
                           "LIMIT 10")

        # Cache query results
        arts = list(arts)
        memcache.set(key, arts)

    return arts


class Ascii(BaseHandler):
    def render_ascii(self, title="", art="", error=""):
        arts = top_arts()

        # Find which arts have coords
        points = filter(None, (a.coords for a in arts))

        # If we have any arts coords, make an image url
        img_url = None
        if points:
            img_url = gmaps_img(points)

        self.render('ascii-form.html', title=title, art=art, error=error,
                    arts=arts, img_url=img_url)

    def get(self):
        self.render_ascii()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            a = Art(title=title, art=art)

            # Look up the user's coordinates from their IP
            coords = get_coords(self.request.remote_addr)

            # If we have coordinates, add them to the Art
            if coords:
                a.coords = coords

            a.put()

            # Rerun the query and update the cache
            top_arts(True)

            self.redirect('/ascii')
        else:
            error = "We need both a title and some artwork!"
            self.render_ascii(title, art, error)


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def as_dict(self):
        date_format = '%b %d, %Y'
        post_dict = {'subject': self.subject,
                     'content': self.content,
                     'created': self.created.strftime(date_format),
                     'last_modified': self.last_modified.strftime(date_format)}
        return post_dict


def age_set(key, val):
    save_time = datetime.utcnow()
    memcache.set(key, (val, save_time))


def age_get(key):
    val_save_tuple = memcache.get(key)

    if val_save_tuple:
        val, save_time = val_save_tuple
        # Compute age in seconds
        age = (datetime.utcnow() - save_time).total_seconds()
    else:
        val, age = None, 0

    return val, age


def add_post(post):
    post.put()
    # Overwrite cache with new posts
    get_posts(update=True)
    return str(post.key().id())


def get_posts(update=False):
    mc_key = 'blogs'
    posts, age = age_get(mc_key)
    posts_query = db.GqlQuery("SELECT * FROM Post "
                              "ORDER BY created DESC LIMIT 10")

    if update or posts is None:
        posts = list(posts_query)
        age_set(mc_key, posts)

    return posts, age


def age_str(age):
    s = 'queried %s seconds ago'
    age = int(age)  # Convert float to int
    if age == 1:
        s = s.replace('seconds', 'second')
    return s % age


class Blog(BaseHandler):
    def get(self):
        posts, age = get_posts()

        if self.format == 'html':
            self.render('blog.html', posts=posts, age=age_str(age))
        elif self.format == 'json':
            self.render_json([p.as_dict() for p in posts])


class NewPost(BaseHandler):
    def render_newpost(self, subject="", content="", error=""):
        self.render('newpost-form.html', subject=subject, content=content,
                    error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = Post(subject=subject, content=content)
            post_id = add_post(post)
            self.redirect('/blog/%s' % post_id)
        else:
            error = "We need both a title and a post!"
            self.render_newpost(subject, content, error)


class Permalink(BaseHandler):
    def get(self, post_id):
        post_key = 'post_' + post_id

        post, age = age_get(post_key)
        if not post:
            post = Post.get_by_id(int(post_id))
            age_set(post_key, post)
            age = 0

        if not post:
            self.error(404)
            return

        if self.format == 'html':
            self.render('permalink.html', post=post, age=age_str(age))
        elif self.format == 'json':
            self.render_json(post.as_dict())


class BlogFlush(BaseHandler):
    def get(self):
        memcache.flush_all()
        self.redirect('/blog')


class Visits(BaseHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')
        if visit_cookie_str:
            cookie_val = v.check_secure_val(visit_cookie_str)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1

        new_cookie_val = v.make_secure_val(str(visits))

        self.response.headers.add_header('Set-Cookie',
                                         'visits=%s' % new_cookie_val)

        if visits > 10:
            self.write("You are the best ever!")
        else:
            self.write("You've been here %s times!" % visits)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/birthday', Birthday),
                               ('/thanks', Thanks),
                               ('/rot13', Rot13),
                               ('/signup', ParamSignup),
                               ('/welcome', Welcome),
                               ('/cookie-signup', CookieSignup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/cookie-welcome', CookieWelcome),
                               ('/ascii', Ascii),
                               ('/visits', Visits),
                               ('/blog/?(?:\.json)?', Blog),
                               ('/blog/newpost', NewPost),
                               ('/blog/([0-9]+)(?:\.json)?', Permalink),
                               ('/blog/flush', BlogFlush)],
                              debug=True)
