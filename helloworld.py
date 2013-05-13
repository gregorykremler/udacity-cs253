import webapp2
import forms as f
import validations as v


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
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


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/birthday', Birthday),
                               ('/thanks', Thanks),
                               ('/rot13', Rot13)],
                              debug=True)
