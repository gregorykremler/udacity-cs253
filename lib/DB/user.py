from google.appengine.ext import db
from lib import utils


class User(db.Model):
    """User entity."""
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    # Query user by name or id
    @classmethod
    def by_id(cls, user_id):
        return cls.get_by_id(user_id)

    @classmethod
    def by_name(cls, username):
        user = db.GqlQuery("SELECT * FROM User WHERE name = :name ",
                           name=username).get()
        return user

    # Create a user object
    @classmethod
    def register(cls, username, password, email=None):
        pw_hash = utils.make_pw_hash(username, password)
        return cls(name=username, pw_hash=pw_hash, email=email)

    # Check password against db hash
    @classmethod
    def authenticate(cls, username, password):
        user = cls.by_name(username)
        if user and utils.valid_pw_hash(username, password, user.pw_hash):
            return user
