from handlers import BaseHandler
from lib.DB.cachedart import CachedArt, top_arts
from lib.DB.mapart import get_coords, gmaps_img
import time


class Cachedscii(BaseHandler):
    """Cached ASCII art forum."""
    def render_cachedscii(self, title="", art="", error=""):
        arts = top_arts()

        # Find which arts have coords
        points = filter(None, (a.coords for a in arts))

        # If we have any art coords, make an img URL
        img_url = None
        if points:
            img_url = gmaps_img(points)

        self.render('cachedscii-form.html', title=title, art=art, error=error,
                    arts=arts, img_url=img_url)

    def get(self):
        self.render_cachedscii()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            a = CachedArt(title=title, art=art)
            # Look up user's coordinates from their IP
            coords = get_coords(self.request.remote_addr)
            if coords:
                a.coords = coords
            a.put()
            # Allow submission time to populate
            time.sleep(.1)
            top_arts(True) # Update the cache
            self.redirect('/cachedscii')
        else:
            error = "We need both a title and some artwork!"
            self.render_cachedscii(title, art, error)
