from django.http import HttpResponseRedirect, QueryDict
from django.core.exceptions import ObjectDoesNotExist
from .models import RealUser, CommentPost
from .SafeError import InputError
import logging
import json
import re

# Get the logger for this class
logger = logging.getLogger(__name__)
MAXIMUM_API_PAYLOAD_LENGTH = 1500


# Utility function to verify API requests
# Checks the payload is valid JSON, and get all the keys from the JSON
# Wrap this function in TRY/EXCEPT as this function will raise exceptions
# if the request payload is invalid or rejected
def verify_json_request(request, key_val):

    # check the payload type is expected
    if request.content_type != 'application/JSON':
        raise InputError('An invalid request payload type was provided',
                         is_message_safe=True)
    # check the payload size is below limit (prevent abuse by sending overly large payload)
    if len(request.body) > MAXIMUM_API_PAYLOAD_LENGTH:
        raise InputError('Payload size exceeded maximum', is_message_safe=True)

    # get payload and ensure that it is correctly formatted as JSON object
    try:
        request_payload = json.loads(request.body)
    except json.JSONDecodeError:
        raise InputError('Payload was not formatted correctly, and could not be parsed', is_message_safe=True)

    for key, val in key_val.items():
        # ensure that the specified keys are present
        if key not in request_payload:
            raise InputError('Payload did not contain the required keys', is_message_safe=True)

        # ensure the values are allowed values (match regex)
        elif not re.fullmatch(val, request_payload[key]):
            raise InputError('Value provided was not an allowed value', is_message_safe=True)

    return request_payload


# Helper function that checks whether the user needs to log in
# returns None if login is required, or User object of logged in user if not
def get_logged_in_user(request):
    if 'session_id' not in request.COOKIES:
        return None

    session_id_raw = request.COOKIES.get('session_id')
    user_id = int(session_id_raw.split('|')[0])

    # Get the user from the database and check the session id
    try:
        user = RealUser.objects.get(pk=user_id)
        if user.attempt_authentication(session_id_raw):
            return user
        else:
            return None
    except ObjectDoesNotExist as e:
        # The session ID does not match with any existing user, have user re-authenticate
        return None
    except Exception as e:
        logger.error(e)
        return None


# Helper function that redirects to the login page while keeping the necessary
# query string parameters and appending the next page to load in the query string
def redirect_to_login(request):
    qd = QueryDict(query_string=request.GET.urlencode(), mutable=True)
    qd['next'] = request.path
    response = HttpResponseRedirect('/login?%s' % qd.urlencode())
    response.delete_cookie('session_id')
    return response


# Helper function that gets all the comments for the given parent post
# The default orders the posts by descending create date, and will only go 5 levels deep.
def get_comment_post(parent_post, order_by='create_date', recursive_limit=5):
    if recursive_limit < 0:
        return []

    data = []
    comments_qs = CommentPost.objects.filter(parent_post_id=parent_post.id)
    # result set was empty; skip over
    if comments_qs:
        comments = comments_qs.order_by(order_by)
        # recurse and append to the data array
        for comment in comments:
            # get & append all the subcomments to create a flat array
            comment_pair = (comment, get_comment_post(comment, recursive_limit=(recursive_limit-1)))
            data.append(comment_pair)

    return data
