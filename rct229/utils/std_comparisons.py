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
        True iff the val is within percent_tolerance of std_val
    """
    return abs(std_val - val) <= (percent_tolerance / 100) * abs(std_val)
