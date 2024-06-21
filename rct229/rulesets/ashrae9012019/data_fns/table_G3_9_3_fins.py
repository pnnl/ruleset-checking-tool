import math

from pint import Quantity
from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_1_fins import (
    FullLoadMotorEfficiency,
)
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.utils.assertions import assert_


def table_G3_9_3_lookup(shaft_input_power: Quantity) -> FullLoadMotorEfficiency:
    """Returns the full-load motor efficiency for motors as required by ASHRAE 90.1 Table G3.9.2
    Parameters
    ----------
    shaft_input_power: Quantity
        shaft input power value

    Returns
    -------
    dict
        {full_load_motor_efficiency_for_modeling - The full load motor efficiency for modeling by Table G3.9.3}

    Raises:
    -------
        TypeError: when the shaft_input_power_mag is less or equal to 0, the function will raise this error
    """

    shaft_input_power_mag = shaft_input_power.to("hp").magnitude
    assert_(
        shaft_input_power_mag > 0,
        "shaft input power is a negative value, incorrect data.",
    )
    shaft_input_power = math.ceil(shaft_input_power_mag / 10) * 10

    if shaft_input_power > 40:
        shaft_input_power = 100

    full_load_motor_efficiency_for_modeling = find_osstd_table_entry(
        [("shaft_input_power", shaft_input_power)],
        osstd_table=data["ashrae_90_1_table_G3_9_3"],
    )["full_load_motor_efficiency_for_modeling"]

    return {
        "full_load_motor_efficiency_for_modeling": full_load_motor_efficiency_for_modeling
    }
