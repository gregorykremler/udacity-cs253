from handlers import BaseHandler
import utils as u

class Birthday(BaseHandler):
    """Validate user birthdate."""
    def render_bday(self, month="", day="", year="", error=""):
        self.render('birthday-form.html', month=month, day=day, year=year,
                    error=error)

    def get(self):
        self.render_bday()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = u.valid_month(user_month)
        day = u.valid_day(user_day)
        year = u.valid_year(user_year)

        if not (month and day and year):
            error = "That doesn't look valid to me, friend."
            self.render_bday(user_month, user_day, user_year, error)
        else:
            self.redirect('/thanks')


class Thanks(BaseHandler):
    def get(self):
        self.render('thanks.html')
