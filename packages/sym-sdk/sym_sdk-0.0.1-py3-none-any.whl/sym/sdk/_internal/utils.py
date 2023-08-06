from functools import wraps


def wrap_with_error(error_class):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception:
                raise error_class()

        return wrapped

    return wrapper
