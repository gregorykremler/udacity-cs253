from handlers import BaseHandler
from google.appengine.ext import db
from lib.DB.post import Post


class Blog(BaseHandler):
    """Blog home page."""
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC "
                            "LIMIT 10")
        if self.format == 'html':
            self.render('blog.html', posts=posts)
        elif self.format == 'json':
            self.render_json([p.as_dict() for p in posts])


class NewPost(BaseHandler):
    """New post composition page."""
    def render_newpost(self, subject="", content="", error=""):
        self.render('newpost-form.html', subject=subject, content=content,
                    error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(subject=subject, content=content)
            p.put()
            # Upon submission redirect to permalink
            post_id = str(p.key().id())
            self.redirect('/blog/%s' % post_id)
        else:
            error = "We need both a title and a post!"
            self.render_newpost(subject, content, error)


class Permalink(BaseHandler):
    """Blog post permalink."""
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))

        if not post:
            self.error(404)
            return

        if self.format == 'html':
            self.render('permalink.html', post=post)
        elif self.format == 'json':
            self.render_json(post.as_dict())
