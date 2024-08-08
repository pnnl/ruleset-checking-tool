from typing import TypedDict

from pint import Quantity
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_object_electric_power import (
    get_fan_object_electric_power,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO


class FanPressureDropCompareCategory:
    """Enumeration class for fan pressure drop types"""

    UNDEFINED: str = "UNDEFINED"
    IDENTICAL: str = "IDENTICAL"
    DIFFERENT: str = "DIFFERENT"


class FanSystemInfoDict(TypedDict, total=False):
    supply_fans_power: Quantity
    supply_fans_airflow: Quantity
    supply_fans_qty: int
    supply_fans_pressure: FanPressureDropCompareCategory
    return_fans_power: Quantity
    return_fans_airflow: Quantity
    return_fans_qty: int
    return_fans_pressure: FanPressureDropCompareCategory
    exhaust_fans_power: Quantity
    exhaust_fans_airflow: Quantity
    exhaust_fans_qty: int
    exhaust_fans_pressure: FanPressureDropCompareCategory
    relief_fans_power: Quantity
    relief_fans_airflow: Quantity
    relief_fans_qty: int
    relief_fans_pressure: FanPressureDropCompareCategory


def get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
    fan_system: dict,
) -> FanSystemInfoDict:
    """
    Get the supply, return, exhaust, and relief total fan power, CFM, quantity, and information about whether the pressure drop is consistent across the fans if more than one for a fan system object.

    Parameters
    ----------
    fan_system: dict fan_system at heating_ventilating_air_conditioning_systems level

    Returns dict that includes supply/return/relief/exhaust fans power/cfm/quantify/pressure_rise keys
    -------

    """

    all_fan_info = {}
    for fan_type in ("supply_fans", "return_fans", "exhaust_fans", "relief_fans"):
        total_fan_power = ZERO.POWER
        total_fan_airflow = ZERO.FLOW
        fan_qty = 0
        design_pressure_rise_data = []

        for fan in find_all(f"$.{fan_type}[*]", fan_system):
            total_fan_power += get_fan_object_electric_power(fan)

            fan_airflow = fan.get("design_airflow")
            if fan_airflow is not None and fan_airflow > ZERO.FLOW:
                total_fan_airflow += fan_airflow
                fan_qty += 1

            design_pressure_rise_data.append(fan.get("design_pressure_rise"))

        fan_pressure_drop = FanPressureDropCompareCategory.UNDEFINED
        if design_pressure_rise_data:
            if None in design_pressure_rise_data:
                fan_pressure_drop = FanPressureDropCompareCategory.UNDEFINED
            elif all(
                design_pressure_rise_data[0] == x for x in design_pressure_rise_data
            ):
                fan_pressure_drop = FanPressureDropCompareCategory.IDENTICAL
            else:
                fan_pressure_drop = FanPressureDropCompareCategory.DIFFERENT

        all_fan_info.update(
            {
                f"{fan_type}_power": total_fan_power,
                f"{fan_type}_airflow": total_fan_airflow,
                f"{fan_type}_qty": fan_qty,
                f"{fan_type}_pressure": fan_pressure_drop,
            }
        )

    return all_fan_info
