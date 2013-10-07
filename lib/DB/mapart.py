from google.appengine.ext import db
from xml.dom import minidom
import urllib2

class MapArt(db.Model):
    """ASCII art entity + art coordinates."""
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    coords = db.GeoPtProperty()
    created = db.DateTimeProperty(auto_now_add=True)


# host.ip.info API returns location data in XML
IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    """Return coordinates from request IP address."""
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except urllib2.URLError:
        return
    if content:
        # Parse XML and return coordinates
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)


# Google Static Maps API draws map with marked coordinates
GMAPS_URL = ("http://maps.googleapis.com/maps/api/staticmap?"
             "size=380x263&sensor=false&")
def gmaps_img(points):
    """Return static map image URL from coordinates list."""
    markers = '&'.join('markers=%s,%s' % (p.lat, p.lon) for p in points)
    return GMAPS_URL + markers
