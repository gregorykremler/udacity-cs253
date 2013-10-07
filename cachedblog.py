from handlers import BaseHandler
from google.appengine.api import memcache
from lib.DB.cachedpost import CachedPost, age_set, age_get, age_str
from lib.DB.cachedpost import add_post, top_posts


class CachedBlog(BaseHandler):
    """Cached blog home page."""
    def get(self):
        posts, age = top_posts()

        if self.format == 'html':
            self.render('cached-blog.html', posts=posts, age=age_str(age))
        elif self.format == 'json':
            self.render_json([p.as_dict() for p in posts])


class NewCachedPost(BaseHandler):
    """New cached post composition page."""
    def render_new_cached_post(self, subject="", content="", error=""):
        self.render('cached-newpost-form.html', subject=subject,
                    content=content, error=error)
    def get(self):
        self.render_new_cached_post()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = CachedPost(subject=subject, content=content)
            # Commit post to db and update memcached
            post_id = add_post(p)
            self.redirect('/cached-blog/%s' % post_id)
        else:
            error = "We need both a title and a post!"
            self.render_new_cached_post(subject, content, error)


class CachedPermalink(BaseHandler):
    """Cached blog post permalink."""
    def get(self, post_id):
        key = 'post_' + post_id
        post, age = age_get(key)

        # Cache each permalink request
        if not post:
            post = CachedPost.get_by_id(int(post_id))
            age_set(key, post)

        if not post:
            self.error(404)
            return

        if self.format == 'html':
            self.render('cached-permalink.html', post=post, age=age_str(age))
        elif self.format == 'json':
            self.render_json(post.as_dict())


class BlogFlush(BaseHandler):
    """Clear memcached."""
    def get(self):
        memcache.flush_all()
        self.redirect('/cached-blog')
