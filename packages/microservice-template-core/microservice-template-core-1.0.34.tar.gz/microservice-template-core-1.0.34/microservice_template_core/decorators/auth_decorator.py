from functools import wraps
from flask import request
from flask_jwt_extended import decode_token
from flask_jwt_extended.jwt_manager import ExpiredSignatureError, InvalidTokenError


def token_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Make endpoint in the Auth Service to validate an Auth Token
            # The endpoint will return details such as User's Account ID

            invalid_msg = {
                'message': 'Invalid token. Registration and / or authentication required',
                'authenticated': False
            }

            expired_msg = {
                'message': 'Expired token. Re authentication required',
                'authenticated': False
            }

            auth_token = request.headers.get('AuthToken', '')
            if auth_token is None:
                return invalid_msg, 401
            try:
                data = decode_token(auth_token, allow_expired=True)
                if data.get('sub'):
                    return fn(data['sub'], *args, **kwargs)
                else:
                    # You can also redirect the user to the login page.
                    return invalid_msg, 401

            except ExpiredSignatureError as err:
                print(err)
                return expired_msg, 401
            except (InvalidTokenError, Exception) as err:
                print(err)
                return invalid_msg, 401
        return decorator
    return wrapper
