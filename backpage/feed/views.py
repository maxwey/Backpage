from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from .models import Post, CommentPost, ParentPost, User, RealUser, PostInteractionTracker
from .SafeError import InputError
from . import utils
import logging
import json

# Get the Logger for this class
logger = logging.getLogger(__name__)


def login(request):
    # Check if login is unnecessary and redirect to another page
    # (don't show login page to logged-in users)
    logged_in_user = utils.get_logged_in_user(request)
    if logged_in_user is not None:
        if 'next' in request.GET:
            qs = request.GET.copy()
            next_page = qs.pop('next')[0]
            if len(qs) > 0:
                return HttpResponseRedirect((next_page + '?%s') % qs.urlencode())
            else:
                return HttpResponseRedirect(next_page)
        else:
            return HttpResponseRedirect('/')

    # Login is required, prepare login page
    # load the html template used for the feed page
    template = loader.get_template('feed/login.html')

    # set the context for the template (define the variables used in the template)
    context = {}

    # Return the HttpResponse to the user with the rendered template
    return HttpResponse(template.render(context, request))


def logout(request):
    logged_in_user = utils.get_logged_in_user(request)
    if logged_in_user is not None:
        logged_in_user.deauthenticate()

    # Redirect to login and clear cookies
    response = HttpResponseRedirect('/login')
    response.delete_cookie('session_id')
    return response


def feed(request):
    # Check if logged in, else redirect to login page
    logged_in_user = utils.get_logged_in_user(request)
    if logged_in_user is None:
        return utils.redirect_to_login(request)

    # load the data from the db
    recent_posts = ParentPost.objects.order_by('-create_date')

    # load the comments
    # TODO: to minimize page load time, load comments as requested rather than all at once
    data = []

    for recent_post in recent_posts:
        post_comment_pair = (recent_post, utils.get_comment_post(recent_post))
        data.append(post_comment_pair)

    # load the html template used for the feed page
    template = loader.get_template('feed/feed.html')

    # set the context for the template (define the variables used in the template)
    context = {
        'logged_in_user': logged_in_user,
        'posts': data
    }

    # Return the HttpResponse to the user with the rendered template
    return HttpResponse(template.render(context, request))


def user_profile(request, user_id):
    # Check if logged in, else redirect to login page
    logged_in_user = utils.get_logged_in_user(request)
    if logged_in_user is None:
        return utils.redirect_to_login(request)

    user = get_object_or_404(User, pk=user_id)

    # load the data from the db
    user_posts = ParentPost.objects.filter(author_id=user_id).order_by('-create_date')

    # load the comments
    # TODO: to minimize page load time, load comments as requested rather than all at once
    data = []

    for recent_post in user_posts:
        post_comment_pair = (recent_post, utils.get_comment_post(recent_post))
        data.append(post_comment_pair)

    # load the user profile template
    template = loader.get_template('feed/userprofile.html')

    # set the context for the template (define the variables that can be used in the template)
    context = {
        'logged_in_user': logged_in_user,
        'user': user,
        'posts': data
    }

    return HttpResponse(template.render(context, request))


#######################################
#    API Endpoints
#######################################


def auth(request):
    try:
        request_payload = utils.verify_json_request(request, {
            'display_name': '[\w\d ]{3,126}',
            'user_name': '[\w\d][\w\d_]{3,126}[\w\d]'
        })

        try:
            # user_name is unique, only 1 or none (none causes Exception to be raised)
            user = RealUser.objects.get(user_name=request_payload['user_name'])
            new_session_id,session_expiration = user.authenticate()
        except ObjectDoesNotExist as e:
            user = RealUser()
            user.name = request_payload['display_name']
            user.user_name = request_payload['user_name']
            user.save()
            new_session_id, session_expiration = user.authenticate()
        except Exception as e:
            logger.error(e)
            raise InputError('Could not get user information.', is_message_safe=True)

        data = {
            'success': True
        }

        response = JsonResponse(data)
        response.set_cookie('session_id', new_session_id, expires=session_expiration)
        return response

    except InputError as e:
        return JsonResponse({'success': False, 'error': e.__str__()}, status=500)
    except Exception as e:
        logger.error('An unexpected error happened when processing an API call', exc_info=e)
        return JsonResponse({'success': False}, status=500)


# Process the API request and return a JSON object with the result from the API request
def post_api(request, post_id):

    # Check if logged in, else fail (no redirect)
    logged_in_user = utils.get_logged_in_user(request)
    if logged_in_user is None:
        response = JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        response.delete_cookie('session_id')
        return response

    try:
        request_payload = utils.verify_json_request(request, {'action': 'like|comment|share'})
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist as e:
            raise InputError('Post specified does not exist', is_message_safe=True)

        data = {
            'success': True,
            'post_id': post_id,
            'action': request_payload['action'],
            'message': 'Success'
        }

        # additional payload content checks
        if request_payload['action'] == 'like':
            data['message'] = 'Post liked!'
        elif request_payload['action'] == 'comment':
            if 'content' not in request_payload:
                raise InputError('Comment must include content', is_message_safe=True)
            content_text = request_payload['content'].strip()
            if len(content_text) == 0:
                raise InputError('Comment text cannot be empty', is_message_safe=True)
            data['content'] = content_text
            data['message'] = 'Comment posted!'
        elif request_payload['action'] == 'share':
            data['message'] = 'Post shared!'

        if logged_in_user.track_enabled:
            entry = PostInteractionTracker()
            entry.user = logged_in_user
            entry.post = post
            entry.action = data['action']
            if 'content' in data:
                entry.content = data['content']
            entry.save()

        # Returns the a response JSON
        return JsonResponse(data)

    except InputError as e:
        return JsonResponse({'success': False, 'error': e.__str__()})
    except Exception as e:
        logger.error('An unexpected error happened when processing an API call', exc_info=e)
        return JsonResponse({'success': False})
