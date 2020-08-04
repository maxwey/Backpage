from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Post, CommentPost, ParentPost, User

# Create your views here.
def index(request):
    # load the data from the db
    recents_posts = ParentPost.objects.order_by('-create_date')

    # load the comments
    # TODO: to minimize page load time, load comments as requested rather than all at once
    data = []
    for recent_post in recents_posts:
        comments_qs = CommentPost.objects.filter(parent_post_id=recent_post.id)
        # result set was empty; skip over
        if comments_qs:
            comments = comments_qs.order_by('create_date')
            data.append((recent_post, comments))
        else:
            data.append((recent_post, ()))

    # load the html template used for the feed page
    template = loader.get_template('feed/index.html')

    # set the context for the template (define the variables used in the template)
    context = {
        'posts': data
    }

    # Return the HttpResponse to the user with the rendered template
    return HttpResponse(template.render(context, request))
