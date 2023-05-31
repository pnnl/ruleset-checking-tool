import functools
import operator
from dataclasses import dataclass

from pint import Quantity

from rct229.schema.config import ureg


class UNIT_SYSTEM:
    """Class representing the two unit systems"""

    IP = "IP"
    SI = "SI"


_UNIT_CONVENTIONS = {
    UNIT_SYSTEM.SI: {
        "transformer_capacity": "V*A",
        "electric_power": "W",
        "volume": "m3",
        "area": "m2",
        "power_density": "W/m2",
        "thermal_transmittance": "W/(m2*K)",
        "linear_thermal_transmittance": "W/(m*K)",
        "cooling_capacity": "W",
        "capacity": "W",
        "volumetric_flow_rate": "m3/s",
        "temperature": "C",
        "cooling_efficiency": "W/W",
        "power_per_volumetric_flow_rate": "W-s/L",
        "power_per_flow_rate": "W-s/L",
        "air_flow_rate": "L/s",
    },
    UNIT_SYSTEM.IP: {
        "transformer_capacity": "V*A",
        "electric_power": "W",
        "volume": "ft3",
        "area": "ft2",
        "power_density": "W/ft2",
        "thermal_transmittance": "Btu/(hr*ft2*R)",
        "linear_thermal_transmittance": "Btu/(hr*ft*R)",
        "cooling_capacity": "ton",
        "capacity": "Btu/hr",
        "volumetric_flow_rate": "cfm",
        "temperature": "F",
        "cooling_efficiency": "kW/ton",
        "power_per_volumetric_flow_rate": "W/gpm",
        "power_per_flow_rate": "W/gpm",
        "air_flow_rate": "cfm",
    },
}


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

    TEMPERATURE = 0 * ureg("K")

    POWER_PER_FLOW = POWER / FLOW


@dataclass(frozen=True)
class CalcQ:
    """Class that encodes the type of quantity along with a pint Quantity"""

    q_type: str
    q: Quantity

    def to_str(self, unit_system=UNIT_SYSTEM.IP) -> str:
        units = _UNIT_CONVENTIONS[unit_system][self.q_type]
        return (
            f"{self.q.to(units).magnitude} {units}"
            if isinstance(self.q, Quantity)
            else str(self.q)
        )


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


def calcq_to_str(unit_system, obj) -> str:
    """Replaces a CalcQ object with its string representation using the units associated
    with its q_type. It will also walk any combination of dicts and lists, replacing
    any CalcQ objects.

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
        retval = None if obj.q is None else obj.to_str(unit_system)
    elif isinstance(obj, list):
        retval = [calcq_to_str(unit_system, item) for item in obj]
    elif isinstance(obj, dict):
        retval = {key: calcq_to_str(unit_system, value) for key, value in obj.items()}
    else:
        retval = obj

    return retval


def pint_sum(qty_list, default=None):
    if len(qty_list) == 0:
        assert default is not None

    return functools.reduce(operator.add, qty_list) if len(qty_list) > 0 else default
