from dataclasses import dataclass
import functools
import operator

from pint import Quantity

from rct229.schema.config import ureg


class UNIT_SYSTEM:
    """Class representing the two unit systems"""

    IP = "IP"
    SI = "SI"


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


@dataclass(frozen=True)
class CalcQ:
    """Class that encodes the type of quantity along with a pint Quantity"""

    q_type: str
    q: Quantity

    def to_str(self, unit_system=UNIT_SYSTEM.IP) -> str:
        return f"{self.q_type}: {unit_system}: {q}"


def calcq_to_q(obj):
    """Replaces a CalcQ object with its quantity. It will also walk any combination
    of dicts and lists, replacing any CalcQ objects.

    Any object other than a CalcQ, list, or dict is simply passed through unchanged.
    This function does not mutate the passed obj.

    Parameters
    ----------
    obj : any
        The object to be converted

    Returns
    -------
    any
        The processed value.

    """
    if isinstance(obj, CalcQ):
        retval = obj.q
    elif isinstance(obj, list):
        retval = [calcq_to_q(item) for item in obj]
    elif isinstance(obj, dict):
        retval = {key: calcq_to_q(value) for key, value in obj.items()}
    else:
        retval = obj

    return retval


def pint_sum(qty_list, default=None):
    if len(qty_list) == 0:
        assert default is not None

    return functools.reduce(operator.add, qty_list) if len(qty_list) > 0 else default
