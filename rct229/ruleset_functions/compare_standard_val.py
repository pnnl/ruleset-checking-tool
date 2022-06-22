from rct229.utils.assertions import assert_
from rct229.utils.std_comparisons import std_equal


def compare_standard_val(val, std_val, operator=None, ahj_ra_compare: bool = False
                ) -> bool:
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
        assert_(operator, "Need to provide operator (operator.lt, operator.gt, operator.le, operator.ge) for "
                          "stringent code comparison")
        return std_equal(std_val, val) or operator(val, std_val)
    else:
        return std_equal(std_val, val)
