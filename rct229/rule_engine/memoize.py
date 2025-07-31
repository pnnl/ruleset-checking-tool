import functools


def memoize(func):
    cache = {}

    @functools.wraps(func)
    def memoized_func(*args):
        key = func.__name__ + str(args)
        if key not in cache:
            cache[key] = func(*args)
        return cache[key]

    return memoized_func
