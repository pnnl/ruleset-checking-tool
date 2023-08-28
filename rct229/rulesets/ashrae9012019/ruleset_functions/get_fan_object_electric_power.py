from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.pint_utils import ZERO

FAN_SPECIFICATION_METHOD = schema_enums["FanSpecificationMethodOptions"]


def get_fan_object_electric_power(fan):
    """
    Get the fan power associated with a fan object.

    Parameters
    ----------
    fan: dict
    A dictionary representing a fan as defined by the ASHRAE229 schema

    Returns
    -------
    fan_elec_power: a pint quantity object with a unit of Btu/hr.
    Raise exception if missing key parameters for calculating the fan power

    """
    fan_elec_power = ZERO.POWER
    fan_spec_method = getattr_(fan, "fan", "specification_method")
    if fan_spec_method == FAN_SPECIFICATION_METHOD.SIMPLE:
        fan_elec_power = getattr_(fan, "design_electric_power", "design_electric_power")
    elif fan_spec_method == FAN_SPECIFICATION_METHOD.DETAILED:
        design_pressure_rise = fan.get("design_pressure_rise", 0.0)
        design_air_flow = fan.get("design_airflow", ZERO.FLOW)
        total_efficiency = fan.get("total_efficiency", 0.0)
        shaft_power = fan.get("shaft_power", ZERO.POWER)
        motor_efficiency = fan.get("motor_efficiency", 0.0)

        if shaft_power > ZERO.POWER and motor_efficiency > 0.0:
            fan_elec_power = shaft_power / motor_efficiency
        elif total_efficiency > 0.0 and design_pressure_rise > 0.0:
            fan_elec_power = (
                design_pressure_rise * design_air_flow / total_efficiency
            ).to("watt")
        else:
            assert_(
                False,
                f"Check Fan: {fan['id']}, Data missing: shaft_power or motor_efficiency are missing or "
                f"equal to 0.0, and total_efficiency or design_pressure_rise are missing or equal to 0.0.",
            )

    return fan_elec_power
