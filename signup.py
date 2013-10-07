from handlers import BaseHandler
import utils as u
from lib.DB.user import User


class Signup(BaseHandler):
    """Validate user registration."""
    def render_signup(self, username="", error_username="", password="",
                      error_password="", verify="", error_verify="", email="",
                      error_email=""):
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

        # Build up dict of error messages to rerender form with on
        # error case (always include username and e-mail, never pw)
        error_params = {'username': self.username, 'email': self.email}

        # If statements will set have_error=True if validation
        # procedures return False
        if not u.valid_username(self.username):
            error_params['error_username'] = "That's not a valid username."
            have_error = True

        # We can either have an invalid pw or the pw's don't match up
        if not u.valid_password(self.password):
            error_params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            error_params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not u.valid_email(self.email):
            error_params['error_email'] = "That's not a valid e-mail."
            have_error = True

        if have_error:
            self.render_signup(**error_params)
        else:
            self.welcome()

    def welcome(self, *a, **kw):
        raise NotImplementedError


class QuerySignup(Signup):
    """Redirect to QueryWelcome."""
    def welcome(self):
        self.redirect('/welcome?username=' + self.username)


class QueryWelcome(BaseHandler):
    """Validate user from query parameter."""
    def get(self):
        username = self.request.get('username')
        if u.valid_username(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('/signup')


class dbSignup(Signup):
    """Store hashed + salted user to datastore."""
    def welcome(self):
        user = User.by_name(self.username)

        # Make sure the user doesn't already exist
        if user:
            error_username = "That user already exists."
            self.render_signup(username=self.username,
                              error_username=error_username, email=self.email)
        else:
            # Store user and set user_id cookie
            user = User.register(self.username, self.password, self.email)
            user.put()
            self.login(user)
            self.redirect('/db-welcome')


class dbWelcome(Signup):
    """Validate user from user_id cookie."""
    def get(self):
        # Check for user_id cookie
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/db-signup')
