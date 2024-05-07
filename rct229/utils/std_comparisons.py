import math
import operator
from pint import Quantity


"""
Global tolerance for equality comparison. Default allows 0.5% variations of generated baseline/proposed from the standard specify value.
"""
DEFAULT_PERCENT_TOLERANCE = 0.5  # %


def std_equal(
    std_val, val, percent_tolerance: float = DEFAULT_PERCENT_TOLERANCE
) -> bool:
    """Determines whether two pint quantities are considered equal, of
    the standard being used

    To determine equality, both quantities are converted to the given units and rounded
    with the given number of digits precision.

    Parameters
    ----------
    std_val : float | Quantity
        A number or pint quantity considered the standard value
    val : float | Quantity
        A number or pint quantity to be compared to the standard value
    percent_tolerance : float
        The allowed percentage difference from the standard value


    Returns
    -------
    bool
        True if the val is within percent_tolerance of std_val
    """
    return abs(std_val - val) <= (percent_tolerance / 100) * abs(std_val)


def std_equal_with_precision(
    val: Quantity, std_val: Quantity, precision: Quantity
) -> bool:
    """Determines whether the model value and standard value are equal with the specified precision.

    Parameters
    ----------
    val: Quantity
        value extracted from model
    std_val : Quantity
        standard value from code
    precision: Quantity
        number of decimal places to round to, and intended units of the comparison

    Returns
    -------
    bool
        True if the modeled value is equal to the standard value within the specified precision
    """
    units = precision.units
    val = val.to(units)
    std_val = std_val.to(units)
    return math.isclose(
        val.magnitude, std_val.magnitude, abs_tol=precision.magnitude / 2
    )


def std_conservative_outcome(
    val: Quantity, std_val: Quantity, conservative_operator_wrt_std: operator
):
    """Determines if the model value has a conservative outcome compared to the standard value.

    Parameters
    ----------
    val: Quantity
        value extracted from model
    std_val : Quantity
        standard value from code
    conservative_operator_wrt_std: operator that results in a conservative outcome compared to the standard value
    """
    return conservative_operator_wrt_std(val, std_val)
