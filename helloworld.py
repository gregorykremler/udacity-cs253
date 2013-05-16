import webapp2
import forms as f
import validations as v


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello, Udacity!')


class Birthday(webapp2.RequestHandler):
    def write_bday(self, error="", month="", day="", year=""):
        self.response.out.write(f.birthday % {"error": error,
                                              "month": v.escape_html(month),
                                              "day": v.escape_html(day),
                                              "year": v.escape_html(year)})

    def get(self):
        self.write_bday()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = v.valid_month(user_month)
        day = v.valid_day(user_day)
        year = v.valid_year(user_year)

        if not (month and day and year):
            self.write_bday("That doesn't look valid to me, friend.",
                            user_month, user_day, user_year)
        else:
            self.redirect("/thanks")


class Thanks(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")


class Rot13(webapp2.RequestHandler):
    def write_rot13(self, text=""):
        self.response.out.write(f.rot13 % {"text": text})

    def get(self):
        self.write_rot13()

    def post(self):
        text = v.rot13(self.request.get('text'))
        self.write_rot13(v.escape_html(text))


class Signup(webapp2.RequestHandler):
    def write_signup(self, username="", error_username="",
                     password="", error_password="",
                     verify="", error_verify="",
                     email="", error_email=""):
        self.response.out.write(f.signup % {"username": username,
                                            "error_username": error_username,
                                            "password": password,
                                            "error_password": error_password,
                                            "verify": verify,
                                            "error_verify": error_verify,
                                            "email": email,
                                            "error_email": error_email})

    def get(self):
        self.write_signup()

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
            self.write_signup(**params)
        else:
            self.redirect("/welcome?username=" + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if v.valid_username(username):
            self.response.out.write('Welcome, %s!' % username)
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/birthday', Birthday),
                               ('/thanks', Thanks),
                               ('/rot13', Rot13),
                               ('/signup', Signup),
                               ('/welcome', Welcome)],
                              debug=True)
