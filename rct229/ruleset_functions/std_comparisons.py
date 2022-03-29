def std_equal(std_val, val, units: str, ndigits: int = 0):
    """Determines whether two pint quantities are considered equal, in the eyes of
    the standard being used

    To determine equality, both quantities are converted to the given units and rounded
    with the given number of digits precision.

    Parameters
    ----------
    std_val : Quantity
        A pint quantity considered the standard value
    val : Quantity
        A pint quantity to be compared to the standard value
    units : str
        A pint units string
    ndigits : int
        The number of digits precision after the decimal point
    Returns
    -------
    bool
        True iff the values are considered equal by the standard
    """
    return round(std_val.to(units).magnitude, ndigits) == round(
        val.to(units).magnitude, ndigits
    )
