import functools
import operator


def pint_sum(qty_list):
    return functools.reduce(operator.add, qty_list)
