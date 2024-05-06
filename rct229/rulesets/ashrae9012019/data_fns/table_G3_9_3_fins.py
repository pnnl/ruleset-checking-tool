from pint import Quantity
from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg


def table_G3_9_3_lookup(shaft_input_power: Quantity) -> dict[str, float]:
    """Returns the full-load motor efficiency for motors as required by ASHRAE 90.1 Table G3.9.2
    Parameters
    ----------
    shaft_input_power: Quantity
        shaft input power value

    Returns
    -------
    dict
        {full_load_motor_efficiency_for_modeling - The full load motor efficiency for modeling by Table G3.9.3}

    """

    if 0 * ureg("hp") <= shaft_input_power <= 10.0 * ureg("hp"):
        shaft_input_power = 10
    elif 10 * ureg("hp") < shaft_input_power <= 20.0 * ureg("hp"):
        shaft_input_power = 20
    elif 20 * ureg("hp") < shaft_input_power <= 30.0 * ureg("hp"):
        shaft_input_power = 30
    elif 30 * ureg("hp") < shaft_input_power <= 40.0 * ureg("hp"):
        shaft_input_power = 40
    elif 40 * ureg("hp") < shaft_input_power:
        shaft_input_power = 100

    full_load_motor_efficiency_for_modeling = find_osstd_table_entry(
        [("shaft_input_power", shaft_input_power)],
        osstd_table=data["ashrae_90_1_table_G3_9_3"],
    )["full_load_motor_efficiency_for_modeling"]

    return {
        "full_load_motor_efficiency_for_modeling": full_load_motor_efficiency_for_modeling
    }
