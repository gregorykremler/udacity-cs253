import webapp2
import os
import jinja2
import json
from lib import utils as u
from lib.DB.user import User


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    """Base class of common convenience functions."""
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
        cookie_val = u.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and u.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    # Override __init__() to check for user_id cookie on each request
    # If request URL ends with .json set 'json' format, else 'html'
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        # if user_id cookie secure and user in db, assign to self.user
        user_id = self.read_secure_cookie('user_id')
        self.user = user_id and User.by_id(int(user_id))

        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'
