from google.appengine.ext import db


class Post(db.Model):
    """Blog post entity."""
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
