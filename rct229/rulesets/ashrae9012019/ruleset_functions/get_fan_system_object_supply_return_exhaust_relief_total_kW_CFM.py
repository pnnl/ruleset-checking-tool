from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_object_electric_power import (
    get_fan_object_electric_power,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all


def get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM(fan_system):
    """
    Get the supply, return, exhaust, and relief total fan power, CFM, quantity, and information about whether the pressure drop is consistent across the fans if more than one for a fan system object.

    Parameters
    ----------
    fan_system: dict fan_system at heating_ventilating_air_conditioning_systems level

    Returns dict dict that includes supply/return/relief/exhaust fans power/cfm/quantify/pressure_rise keys
    -------

    """
    all_fan_info = {}

    for fan_type in ("supply_fans", "return_fans", "exhaust_fans", "relief_fans"):
        total_fan_power = 0.0 * ureg("W")
        total_fan_cfm = 0.0 * ureg("cfm")
        fan_qty = 0
        design_pressure_rise_tempo = []

        for fan in find_all(f"$.{fan_type}[*]", fan_system):
            fan_elec_power = get_fan_object_electric_power(fan)
            if fan_elec_power:
                total_fan_power += fan_elec_power

            fan_cfm = fan.get("design_airflow")
            if fan_cfm is not None and fan_cfm > 0.0 * ureg("cfm"):
                total_fan_cfm += fan_cfm
                fan_qty += 1

            design_pressure_rise_tempo.append(fan.get("design_pressure_rise"))

        if None in design_pressure_rise_tempo:
            fan_pressure_drop = "UNDEFINED"
        elif design_pressure_rise_tempo and all(
            design_pressure_rise_tempo[0] == x for x in design_pressure_rise_tempo
        ):
            fan_pressure_drop = "IDENTICAL"
        else:
            fan_pressure_drop = "DIFFERENT"

        all_fan_info.update(
            {
                f"{fan_type}_power": total_fan_power,
                f"{fan_type}_cfm": total_fan_cfm,
                f"{fan_type}_qty": fan_qty,
                f"{fan_type}_pressure": fan_pressure_drop,
            }
        )

    return all_fan_info
