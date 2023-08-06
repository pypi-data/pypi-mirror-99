from functools import wraps
from flask import request
from flask_jwt_extended import decode_token
from flask_jwt_extended.jwt_manager import ExpiredSignatureError, InvalidTokenError


def token_required(controller_function):
    @wraps(controller_function)
    def wrapper_function(*args, **kwargs):
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
            token = auth_token[0]
            data = decode_token(token)
            if data.get('username'):
                controller_function(data['username'], *args, **kwargs)
            else:
                # You can also redirect the user to the login page.
                return invalid_msg, 401

        except ExpiredSignatureError:
            return expired_msg, 401
        except (InvalidTokenError, Exception) as e:
            return invalid_msg, 401
