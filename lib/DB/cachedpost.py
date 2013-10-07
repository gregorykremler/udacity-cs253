from google.appengine.ext import db
from google.appengine.api import memcache
from datetime import datetime
import logging


class CachedPost(db.Model):
    """Cached blog post entity."""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def as_dict(self):
        date_format = '%b %d, %Y'
        post_dict = {'subject': self.subject,
                     'content': self.content,
                     'created': self.created.strftime(date_format),
                     'last_modified': self.last_modified.strftime(date_format)}
        return post_dict


def age_set(key, val):
    """Store val + time stored to memcache."""
    time_stored = datetime.utcnow()
    memcache.set(key, (val, time_stored))


def age_get(key):
    """Return val + age from memcache."""
    result = memcache.get(key)
    # If we have a val, calc its duration in memcache
    if result:
        val, time_stored = result
        age = (datetime.utcnow() - time_stored).total_seconds()
    else:
        val, age = None, 0
    return val, age


def age_str(age):
    """Return memcache duration str."""
    s = "queried %d seconds ago."
    age = int(age)
    if age == 1:
        s = s.replace('seconds', 'second')
    elif age > 60:
        to_min = lambda sec: sec / 60
        s = "queried %d minutes ago."
        age = to_min(age)
        if age == 1:
            s = s.replace('minutes', 'minute')
    return s % age


def top_posts(update=False):
    """Return posts + age from memcache."""
    key = 'top_posts'
    posts, age = age_get(key)
    # Run query only if it hasn't been cached or to update memcache
    if posts is None or update:
        logging.info("DB QUERY") # remove logging before commit
        posts = db.GqlQuery("SELECT * FROM CachedPost ORDER BY created DESC "
                            "LIMIT 10")
        # Cache the query results
        posts = list(posts)
        age_set(key, posts)
    return posts, age


def add_post(post):
    """Store post to db, update memcache and return post_id."""
    post.put()
    top_posts(True)
    return str(post.key().id())
