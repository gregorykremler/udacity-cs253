from handlers import BaseHandler
from google.appengine.ext import db
from lib.DB.mapart import MapArt, get_coords, gmaps_img


class Mapscii(BaseHandler):
    """ASCII art forum + submissions map."""
    def render_mapscii(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM MapArt ORDER BY created DESC "
                           "LIMIT 10")
        arts = list(arts) # Cache the query results

        # Find which arts have coords
        points = filter(None, (a.coords for a in arts))

        # If we have any art coords, make an img URL
        img_url = None
        if points:
            img_url = gmaps_img(points)

        self.render('mapscii-form.html', title=title, art=art, error=error,
                    arts=arts, img_url=img_url)

    def get(self):
        self.render_mapscii()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            a = MapArt(title=title, art=art)
            # Look up user's coordinates from their IP
            coords = get_coords(self.request.remote_addr)
            if coords:
                a.coords = coords
            a.put()
            self.redirect('/mapscii')
        else:
            error = "We need both a title and some artwork!"
            self.render_mapscii(title, art, error)
