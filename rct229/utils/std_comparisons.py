import operator
from pint import Quantity
from decimal import Decimal, ROUND_HALF_UP
from rct229.schema.config import ureg


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

    tolerance = (percent_tolerance / 100) * abs(std_val)

    # If the units of std_value are absolute temperature, the tolerance must be in differential temperature
    if (
        isinstance(std_val, Quantity)
        and std_val.dimensionality == ureg.kelvin.dimensionality
    ):
        tolerance = tolerance.magnitude * ureg("delta_degC")

    return abs(std_val - val) <= tolerance


def std_equal_with_precision(
    val: Quantity | float | int,
    std_val: Quantity | float | int,
    precision: Quantity | float | int,
) -> bool:
    """Determines whether the model value and standard value are equal with the specified precision. If any of the function inputs are a Quantity type, then all function inputs must be Quantity.

    Parameters
    ----------
    val: Quantity | float | int
        value extracted from model
    std_val : Quantity | float | int
        standard value from code
    precision: Quantity | float | int
        number of decimal places or significant value to round to, and intended units of the comparison

    Returns
    -------
    bool
        True if the modeled value is equal to the standard value within the specified precision
    """
    # Check if all or none of the arguments are Quantity types
    are_quantities = [isinstance(arg, Quantity) for arg in [val, std_val, precision]]
    if not (all(are_quantities) or not any(are_quantities)):
        raise TypeError(
            "Arguments must be consistent in type: all Quantity or all non-Quantity."
        )

    # Determine if the values are pint Quantities and handle accordingly
    if (
        isinstance(val, Quantity)
        and isinstance(std_val, Quantity)
        and isinstance(precision, Quantity)
    ):
        units = precision.units
        val = val.to(units)
        std_val = std_val.to(units)
        val_magnitude = Decimal(str(val.magnitude))
        std_val_magnitude = Decimal(str(std_val.magnitude))
        precision_magnitude = Decimal(str(precision.magnitude))
    else:
        val_magnitude = Decimal(str(val))
        std_val_magnitude = Decimal(str(std_val))
        precision_magnitude = Decimal(str(precision))

    precision_magnitude = precision_magnitude.normalize()

    # Determine rounding precision based on whether precision is a whole number or a decimal
    if precision_magnitude.as_tuple().exponent < 0:
        # Decimal places (e.g., 0.01)
        precision_decimal_places = abs(precision_magnitude.as_tuple().exponent)
        rounding_precision = f"1E-{str(precision_decimal_places)}"
    else:
        # Whole number (e.g., 10, 100)
        rounding_precision = f"1E+{str(int(precision_magnitude.log10()))}"

    # Round both values to the specified precision
    val_rounded = val_magnitude.quantize(
        Decimal(rounding_precision), rounding=ROUND_HALF_UP
    )
    std_val_rounded = std_val_magnitude.quantize(
        Decimal(rounding_precision), rounding=ROUND_HALF_UP
    )

    # Compare the rounded values
    return val_rounded == std_val_rounded


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
