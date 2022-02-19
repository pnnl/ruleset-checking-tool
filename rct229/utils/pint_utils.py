import functools
import operator


def pint_sum(qty_list, default=None):
    if len(qty_list) == 0:
        assert default is not None

    return functools.reduce(operator.add, qty_list) if len(qty_list) > 0 else default
