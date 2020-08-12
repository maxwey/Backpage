from django.db import models
from django.templatetags.static import static

# Create your models here.


class User(models.Model):
    """
    This class represents a single user. Each user has their own associated data
    such as display name, picture, friends, etc.
    """
    # Name of the user
    name = models.CharField(max_length=128)
    # Introduction text about user
    intro_text = models.TextField()
    # Portrait picture
    portrait = models.ImageField(blank=True, null=True, upload_to='portraits')
    # TODO: Is a verified user (gets a special badge)
    is_verified = models.BooleanField(default=False)
    # TODO: Friends/Connections. Need some many-to-many relationship

    def get_portrait_url(self):
        try:
            return self.portrait.url
        except:
            return static('img/default_user_profile.png')

    def __str__(self):
        return "User{%d, %s}" % (self.id, self.name)


class Post(models.Model):
    """
    This class represents a single user Post, with all associated media, text
    author data as well as interaction data such as likes and shares
    """
    # Post create date/time
    create_date = models.DateTimeField('date created')
    # Post content
    text = models.TextField()
    # FK to author
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Post{%d, %s, %s}" % (self.id, self.author, self.text[:20])


class CommentPost(Post):
    """
    This class represents a comment, with all associated media, text, author
    data as well as interaction data, such as likes and shares.
    Comments only differ from a Post in that they must link to another Post
    """

    parent_post = models.ForeignKey(Post, related_query_name="comment_parent_post", on_delete=models.CASCADE)

    def __str__(self):
        return "CommentPost{%d, %d, %s, %s}" % (self.id, self.parent_post.id, self.author, self.text[:20])


class ParentPost(Post):
    """
    This class represents a "parent post". That is, any post that was made that is
    not a comment.
    """

    def __str__(self):
        return "ParentPost{%d, %s, %s}" % (self.id, self.author, self.text[:20])