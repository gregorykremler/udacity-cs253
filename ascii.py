from handlers import BaseHandler
from google.appengine.ext import db
from lib.DB.art import Art


class Ascii(BaseHandler):
    """ASCII art forum."""
    def render_ascii(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC "
                           "LIMIT 10")
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
