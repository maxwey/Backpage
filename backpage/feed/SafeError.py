# SafeError are a subclass of Errors that are User data safe.
# This means that they contain methods that allow these exceptions to be raised without exposing
# information to the users.


class SafeError(Exception):
    """Base class for SafeError"""

    def __init__(self, message, is_message_safe=False):
        self.message = message
        self.is_message_safe = is_message_safe

    def __str__(self):
        if self.is_message_safe:
            return self.message
        else:
            return 'Error message not shown'

    def __repr__(self):
        return self.__class__.__name__ + ': ' + self.__str__()


class InputError(SafeError):
    """An error raised when an input is invalid or could not be parsed"""
    pass
