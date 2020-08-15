from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from .models import Post, CommentPost, ParentPost, User, RealUser
from .SafeError import InputError
from . import utils
import logging
import json

# Get the Logger for this class
logger = logging.getLogger(__name__)


# Helper function for the views to help with
def check_if_login_required(request):
    if 'session_id' not in request.COOKIES:
        return True

    session_id_raw = request.COOKIES.get('session_id').split('|')
    user_id = int(session_id_raw[0])
    session_id = session_id_raw[1]

    # Get the user from the database and check the session id
    try:
        user = RealUser.objects.get(pk=user_id)
        return user.attempt_authentication(session_id)
    except ObjectDoesNotExist as e:
        # The session ID does not match with any existing user, have user re-authenticate
        return True
    except Exception as e:
        logger.error(e)
        return True


def login(request):
    # Check if login is unnecessary and redirect to another page
    if not check_if_login_required(request):
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


def feed(request):
    # Check if logged in, else redirect to login page
    if check_if_login_required(request):
        qd = QueryDict(query_string=request.GET.urlencode(), mutable=True)
        qd['next'] = request.path
        response = HttpResponseRedirect('/login?%s' % qd.urlencode())
        response.delete_cookie('session_id')
        return response

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
    template = loader.get_template('feed/feed.html')

    # set the context for the template (define the variables used in the template)
    context = {
        'posts': data
    }

    # Return the HttpResponse to the user with the rendered template
    return HttpResponse(template.render(context, request))


def user_profile(request, user_id):
    # Check if logged in, else redirect to login page
    if check_if_login_required(request):
        qd = QueryDict(query_string=request.GET.urlencode(),mutable=True)
        qd['next'] = request.path
        response = HttpResponseRedirect('/login?%s' % qd.urlencode())
        response.delete_cookie('session_id')
        return response

    user = get_object_or_404(User, pk=user_id)

    # load the user profile template
    template = loader.get_template('feed/userprofile.html')

    # set the context for the template (define the variables that can be used in the template)
    context = {
        'user': user
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
            # user_name is unique, only 1 or none
            user = RealUser.objects.get(user_name=request_payload['user_name'])
            if user is not None:
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

    # Check if logged in, else fail
    if check_if_login_required(request):
        response = HttpResponse('Unauthorized', status=401)
        response.delete_cookie('session_id')
        return response

    try:
        request_payload = utils.verify_json_request(request, {'action': 'like|comment|share'})

        data = {
            'success': True,
            'post_id': post_id,
            'action': request_payload['action']
        }

        # additional payload content checks
        if request_payload['action'] == 'like':
            pass
        elif request_payload['action'] == 'COMMENT':
            if 'content' not in request_payload:
                raise InputError('Comment must include content', is_message_safe=True)
            content_text = request_payload['content'].strip()
            if len(content_text) == 0:
                raise InputError('Comment text cannot be empty', is_message_safe=True)
            data['content'] = content_text
        elif request_payload['action'] == 'SHARE':
            pass

        # Returns the a response JSON
        return JsonResponse(data)

    except InputError as e:
        return JsonResponse({'success': False, 'error': e.__str__()})
    except Exception as e:
        logger.error('An unexpected error happened when processing an API call', exc_info=e)
        return JsonResponse({'success': False})
