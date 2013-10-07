from google.appengine.ext import db


class Art(db.Model):
    """ASCII art entity."""
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
