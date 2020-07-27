from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Post, User

# Create your views here.
def index(request):
    # load the data from the db
    recents_posts = Post.objects.order_by('-create_date')

    # load the html template used for the feed page
    template = loader.get_template('feed/index.html')

    # set the context for the template (define the variables used in the template)
    context = {
        'posts': recents_posts
    }

    # Return the HttpResponse to the user with the rendered template
    return HttpResponse(template.render(context, request))
