import operator
from functools import partial

from rct229.utils.std_comparisons import AHJ_RA_COMPARE, std_equal


def compare_standard_val(ahj_ra_compare, val, std_val, operator=None) -> bool:
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
    ahj_ra_compare: Boolean
        flag True: stringent code check, False: regular equality check

    Returns
    -------
    bool
        True if the comparison matches to the defined relationship or equal.
    """
    if ahj_ra_compare:
        return std_equal(std_val, val) or operator(val, std_val)
    else:
        return std_equal(std_val, val)


def compare_standard_val_strict(ahj_ra_compare, val, std_val, operator=None) -> bool:
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
    ahj_ra_compare: Boolean
        flag True: stringent code check, False: regular equality check
    strict_mode: Boolean
        flat True: compare do not allow tolerance, False: compare allow tolerance

    Returns
    -------
    bool
        True if the comparison matches to the defined relationship or equal.
    """
    if ahj_ra_compare:
        return operator(val, std_val)
    else:
        return std_val == val


# less than
std_lt = partial(
    compare_standard_val, ahj_ra_compare=AHJ_RA_COMPARE, operator=operator.lt
)

std_strict_lt = partial(
    compare_standard_val_strict, ahj_ra_compare=AHJ_RA_COMPARE, operator=operator.lt
)

# less equal
std_le = partial(
    compare_standard_val, ahj_ra_compare=AHJ_RA_COMPARE, operator=operator.le
)

std_strict_le = partial(
    compare_standard_val_strict, ahj_ra_compare=AHJ_RA_COMPARE, operator=operator.le
)

# greater than
std_gt = partial(
    compare_standard_val, ahj_ra_compare=AHJ_RA_COMPARE, operator=operator.gt
)

std_strict_gt = partial(
    compare_standard_val_strict, ahj_ra_compare=AHJ_RA_COMPARE, operator=operator.le
)

# greater equal
std_ge = partial(
    compare_standard_val, ahj_ra_compare=AHJ_RA_COMPARE, operator=operator.ge
)

std_strict_ge = partial(
    compare_standard_val_strict, ahj_ra_compare=AHJ_RA_COMPARE, operator=operator.ge
)
