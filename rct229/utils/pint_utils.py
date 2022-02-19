import functools
import operator


def pint_sum(qty_list, initializer=None):
    return functools.reduce(operator.add, qty_list, initializer)
