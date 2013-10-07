from google.appengine.ext import db
from google.appengine.api import memcache


class CachedArt(db.Model):
    """Cached ASCII art entity."""
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    coords = db.GeoPtProperty()
    created = db.DateTimeProperty(auto_now_add=True)


def top_arts(update=False):
    """Return arts from memcache."""
    key = 'top_arts'
    arts = memcache.get(key)
    # Run query only if it hasn't been cached or to update memcache
    if arts is None or update:
        arts = db.GqlQuery("SELECT * FROM CachedArt ORDER BY created DESC "
                           "LIMIT 10")
        # Cache the query results
        arts = list(arts)
        memcache.set(key, arts)
    return arts
