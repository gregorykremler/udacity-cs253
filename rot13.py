from handlers import BaseHandler
from lib import utils as u


class Rot13(BaseHandler):
    """Apply Rot13 cipher to text."""
    def render_rot13(self, text=""):
        self.render('rot13-form.html', text=text)

    def get(self):
        self.render_rot13()

    def post(self):
        text = u.rot13(self.request.get('text'))
        self.render_rot13(text)
