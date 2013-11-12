from handlers import BaseHandler
from lib import utils as u


class Visits(BaseHandler):
    """Set hashed visits cookie."""
    def render_visits(self, visits):
            self.render('visits.html', visits=visits)

    def get(self):
        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')

        # Authenticate visits cookie
        if visit_cookie_str:
            cookie_val = u.check_secure_val(visit_cookie_str)
            if cookie_val:
                visits = int(cookie_val)

        # visits is either 0 or cookie val
        visits += 1

        new_cookie_val = u.make_secure_val(str(visits))
        self.response.headers.add_header('Set-Cookie',
                                         'visits=%s' % new_cookie_val)
        self.render_visits(visits)
