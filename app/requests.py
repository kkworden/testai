from flask import request
from functools import wraps
from .responses import error


def require_params(params_list):
    '''
    Decorator function to throw an error if a required body parameter was not supplied.
    '''
    def decorator(view_function):

        @wraps(view_function)
        def wrapper(*args, **kwargs):
            missing_params = [p for p in params_list if p not in request.json]
            if missing_params:
                return error(f'Missing parameters: {missing_params}')
            return view_function(*args, **kwargs)

        return wrapper

    return decorator
