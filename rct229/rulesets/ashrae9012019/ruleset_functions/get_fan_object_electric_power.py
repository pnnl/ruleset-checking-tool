from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import ZERO


FAN_SPECIFICATION_METHOD = schema_enums["FanSpecificationMethodOptions"]
CONVERSION_FACTOR = 8250 * ureg("hr*ft/Btu")


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
    None if missing key parameters for calculating the fan power

    """
    fan_elec_power = None
    fan_spec_method = getattr_(fan, "fan", "specification_method")
    if fan_spec_method == FAN_SPECIFICATION_METHOD.SIMPLE:
        # fan_elec_power = getattr_(fan, "fan", "design_electric_power")
        fan_elec_power = fan.get("design_electric_power", None)
    elif fan_spec_method == FAN_SPECIFICATION_METHOD.DETAILED:
        design_pressure_rise = fan.get("design_pressure_rise", ZERO.LENGTH)
        total_efficiency = fan.get("total_efficiency", 0.0)
        input_power = fan.get("input_power", ZERO.POWER)
        motor_efficiency = fan.get("motor_efficiency", 0.0)

        if input_power > 0.0 and motor_efficiency > 0.0:
            fan_elec_power = input_power / motor_efficiency
        elif total_efficiency > 0.0 and design_pressure_rise > 0.0:
            fan_elec_power = design_pressure_rise / (
                CONVERSION_FACTOR * total_efficiency
            )

    return fan_elec_power
