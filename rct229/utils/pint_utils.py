import functools
import operator

from rct229.schema.config import ureg


class ZERO:
    """Class holding zero values for various pint quantities"""

    LENGTH = 0 * ureg("ft")
    AREA = LENGTH * LENGTH
    VOLUME = AREA * LENGTH

    POWER = 0 * ureg("Btu/hr")
    THERMAL_CAPACITY = POWER / ureg("ft2")
    POWER_PER_AREA = THERMAL_CAPACITY

    U_FACTOR = ureg("Btu/(hr*ft2*degR)")
    UA = U_FACTOR * AREA
    FLOW = VOLUME / ureg("minute")

    
class ONE:
    """Class holding one values for various pint quantities"""
    LENGTH = 1.0 * ureg("ft")
    AREA = LENGTH * LENGTH
    VOLUME = AREA * LENGTH

    POWER = 1.0 * ureg("Btu/hr")
    THERMAL_CAPACITY = POWER / ureg("ft2")
    POWER_PER_AREA = THERMAL_CAPACITY

    U_FACTOR = ureg("Btu/(hr*ft2*degR)")
    UA = U_FACTOR * AREA
    FLOW = VOLUME / ureg("minute")

def pint_sum(qty_list, default=None):
    if len(qty_list) == 0:
        assert default is not None

    return functools.reduce(operator.add, qty_list) if len(qty_list) > 0 else default
