from .SafeError import InputError
import json
import re

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
