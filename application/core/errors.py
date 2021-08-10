class CustomException(Exception):
    status_code = 400
    message = None

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


class UserAlreadyExists(CustomException):
    status_code = 409
    message = 'User with this username already exists'


class UserNotFound(CustomException):
    status_code = 422
    message = 'User not found'


class ItemNotFound(CustomException):
    status_code = 422
    message = 'Item not found'


class WrongCredentials(CustomException):
    status_code = 401
    message = 'Wrong credentials provided'


class UnauthorizedSendLink(CustomException):
    status_code = 401
    message = 'Send link failed authentication '


class WrongRecipientUser(CustomException):
    status_code = 409
    message = 'User already is the owner of the item'
