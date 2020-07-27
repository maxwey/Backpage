from django.db import models

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
