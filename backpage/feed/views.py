from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import Post, CommentPost, ParentPost, User
from .SafeError import InputError
import logging
import json

# Get the Logger for this class
logger = logging.getLogger(__name__)


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


# Process the API request and return a JSON object with the result from the API request
def post_api(request, post_id):
    MAXIMUM_API_PAYLOAD_LENGTH = 1500


    try:
        # check the payload type is expected
        if request.content_type != 'application/JSON':
            raise InputError('An invalid request payload type was provided', is_message_safe=True)
        # check the payload size is below limit (prevent abuse by sending overly large payload)
        if len(request.body) > MAXIMUM_API_PAYLOAD_LENGTH:
            raise InputError('Payload size exceeded maximum', is_message_safe=True)

        # get payload and ensure that it is correctly formatted as JSON object
        request_payload = ''
        try:
            request_payload = json.loads(request.body)
        except json.JSONDecodeError:
            raise InputError('Payload was not formatted correctly, and could not be parsed', is_message_safe=True)

        data = {
            'success': True,
            'post': post_id
        }

        # check that the required keys are provided as part of the payload
        try:
            if request_payload['action'].upper() == 'LIKE':
                data['action'] = 'LIKE'
            elif request_payload['action'].upper() == 'COMMENT':
                data['action'] = 'COMMENT'
                if 'content' not in request_payload:
                    raise InputError('Comment must include content', is_message_safe=True)
                content_text = request_payload['content'].strip()
                if len(content_text) == 0:
                    raise InputError('Comment text cannot be empty', is_message_safe=True)
                data['content'] = content_text
            elif request_payload['action'].upper() == 'SHARE':
                data['action'] = 'SHARE'
            else:
                raise InputError('API action provided was not recognized', is_message_safe=True)
        except KeyError:
            raise InputError('Payload did not contain the required keys', is_message_safe=True)

        # Returns the a response JSON
        return JsonResponse(data)

    except InputError as e:
        return JsonResponse({'success': False, 'error': e.__str__()})
    except Exception as e:
        logger.error('An unexpected error happened when processing an API call', exc_info=e)
        return JsonResponse({'success': False})
