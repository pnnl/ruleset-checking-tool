import operator
from functools import partial

from rct229.utils.std_comparisons import std_equal


def compare_standard_val(val, std_val, operator=None) -> bool:
    """Determines whether the model value and standard value are equal or match to user specified relationship
    if stringent code check applied.

    Parameters
    ----------
    val: Quantity
        value extracted from model
    std_val : Quantity
        standard value from code
    operator: operator
        defined user relationship, it should be either operator.lt,operator.le, operator.gt, operator.ge

    Returns
    -------
    bool
        True if the comparison matches to the defined relationship or equal.
    """
    return std_equal(std_val, val) or operator(val, std_val)


def compare_standard_val_strict(val, std_val, operator=None) -> bool:
    """Determines whether the model value and standard value are equal or match to user specified relationship
    if stringent code check applied.

    Parameters
    ----------
    val: Quantity
        value extracted from model
    std_val : Quantity
        standard value from code
    operator: operator
        defined user relationship, it should be either operator.lt,operator.le, operator.gt, operator.ge

    Returns
    -------
    bool
        True if the comparison matches to the defined relationship or equal.
    """
    return operator(val, std_val)


# less than
std_lt = partial(compare_standard_val_strict, operator=operator.lt)

# less equal
std_le = partial(compare_standard_val, operator=operator.le)

# greater than
std_gt = partial(compare_standard_val_strict, operator=operator.gt)

# greater equal
std_ge = partial(compare_standard_val, operator=operator.ge)
