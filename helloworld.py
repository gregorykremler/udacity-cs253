import os
import webapp2
import jinja2
import validations as v
from google.appengine.ext import db


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
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username=username,
                      email=email)

        if not v.valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not v.valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not v.valid_email(email):
            params['error_email'] = "That's not a valid e-mail."
            have_error = True

        if have_error:
            self.render_signup(**params)
        else:
            self.redirect('/welcome?username=' + username)


class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if v.valid_username(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('/signup')


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class Ascii(BaseHandler):
    def render_ascii(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                           "ORDER BY created DESC ")

        self.render('ascii-form.html', title=title, art=art, error=error,
                    arts=arts)

    def get(self):
        self.render_ascii()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            a = Art(title=title, art=art)
            a.put()
            self.redirect('/ascii')
        else:
            error = "We need both a title and some artwork!"
            self.render_ascii(title, art, error)


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)


class Blog(BaseHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created DESC LIMIT 10")
        self.render('blog.html', posts=posts)


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
            p = Post(subject=subject, content=content)
            p.put()
            post_id = str(p.key().id())
            self.redirect('/blog/%s' % post_id)
        else:
            error = "We need both a title and a post!"
            self.render_newpost(subject, content, error)


class Permalink(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render('permalink.html', post=post)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/birthday', Birthday),
                               ('/thanks', Thanks),
                               ('/rot13', Rot13),
                               ('/signup', Signup),
                               ('/welcome', Welcome),
                               ('/ascii', Ascii),
                               ('/blog/?', Blog),
                               ('/blog/newpost', NewPost),
                               ('/blog/([0-9]+)', Permalink)],
                              debug=True)
