import functools


def takes(*correct_args):
    def wraps(func):
        @functools.wraps(func)
        def wrapper(*args):
            for have, need in zip(args, correct_args):
                if not isinstance(have, need):
                    raise TypeError
            return func(*args)

        return wrapper

    return wraps

