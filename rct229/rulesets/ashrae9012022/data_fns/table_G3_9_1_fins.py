from typing import TypedDict

from pint import Quantity
from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg
from rct229.utils.assertions import assert_


class FullLoadMotorEfficiency(TypedDict):
    full_load_motor_efficiency_for_modeling: float


def table_G3_9_1_lookup(
    shaft_input_power: Quantity,
) -> FullLoadMotorEfficiency:
    """Returns the full-load motor efficiency for motors as required by ASHRAE 90.1 Table G3.9.1
    Parameters
    ----------
    shaft_input_power: Quantity
        shaft input power value

    Returns
    -------
    dict
        {full_load_motor_efficiency_for_modeling - The full load motor efficiency by Table G3.9.1}

    """

    assert_(
        shaft_input_power > 0.0 * ureg("hp"),
        "The `shaft_input_power` must be greater than 0.0 hp.",
    )
    shaft_input_power_mag = shaft_input_power.magnitude

    if shaft_input_power_mag <= 1.0:
        minimum_shaft_input_power = 1.0
    elif shaft_input_power_mag <= 1.5:
        minimum_shaft_input_power = 1.5
    elif shaft_input_power_mag <= 2.0:
        minimum_shaft_input_power = 2.0
    elif shaft_input_power_mag <= 3.0:
        minimum_shaft_input_power = 3.0
    elif shaft_input_power_mag <= 5.0:
        minimum_shaft_input_power = 5.0
    elif shaft_input_power_mag <= 7.5:
        minimum_shaft_input_power = 7.5
    elif shaft_input_power_mag <= 10.0:
        minimum_shaft_input_power = 10.0
    elif shaft_input_power_mag <= 15.0:
        minimum_shaft_input_power = 15.0
    elif shaft_input_power_mag <= 20.0:
        minimum_shaft_input_power = 20.0
    elif shaft_input_power_mag <= 25.0:
        minimum_shaft_input_power = 25.0
    elif shaft_input_power_mag <= 30.0:
        minimum_shaft_input_power = 30.0
    elif shaft_input_power_mag <= 40.0:
        minimum_shaft_input_power = 40.0
    elif shaft_input_power_mag <= 50.0:
        minimum_shaft_input_power = 50.0
    elif shaft_input_power_mag <= 60.0:
        minimum_shaft_input_power = 60.0
    elif shaft_input_power_mag <= 75.0:
        minimum_shaft_input_power = 75.0
    elif shaft_input_power_mag <= 100.0:
        minimum_shaft_input_power = 100.0
    elif shaft_input_power_mag <= 125.0:
        minimum_shaft_input_power = 125.0
    elif shaft_input_power_mag <= 150.0:
        minimum_shaft_input_power = 150.0
    else:
        minimum_shaft_input_power = 200.0

    full_load_motor_efficiency_for_modeling = find_osstd_table_entry(
        [("shaft_input_power", minimum_shaft_input_power)],
        osstd_table=data["ashrae_90_1_table_G3_9_1"],
    )["full_load_motor_efficiency_for_modeling"]

    return {
        "full_load_motor_efficiency_for_modeling": full_load_motor_efficiency_for_modeling
    }
