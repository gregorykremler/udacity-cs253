from handlers import BaseHandler


class Logout(BaseHandler):
    """Delete user_id cookie."""
    def get(self):
        self.logout()
        self.redirect('/db-signup')
