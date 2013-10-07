from handlers import BaseHandler
from lib.DB.user import User


class Login(BaseHandler):
    """Set user_id cookie."""
    def render_login(self, username="", password="", error=""):
        self.render('login-form.html', username=username, password=password,
                    error=error)

    def get(self):
        self.render_login()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        # If user successfully authenticated set user_id cookie
        user = User.authenticate(username, password)
        if user:
            self.login(user)
            self.redirect('/db-welcome')
        else:
            error = "Invalid login"
            self.render_login(username=username, error=error)
