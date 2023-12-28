from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg


def table_G3_9_1_lookup(shaft_input_power):
    """Returns the full-load motor efficiency for motors as required by ASHRAE 90.1 Table G3.9.1
    Parameters
    ----------
    shaft_input_power: Quantity
        shaft input power value

    Returns
    -------
    dict
        {nominal_full_load_efficiency - The full load motor efficiency by Table G3.9.1}

    """

    if 0 * ureg("hp") <= shaft_input_power < 1.0 * ureg("hp"):
        minimum_shaft_input_power = 0.0
    elif 1.0 * ureg("hp") <= shaft_input_power < 1.5 * ureg("hp"):
        minimum_shaft_input_power = 1.0
    elif 1.5 * ureg("hp") <= shaft_input_power < 2.0 * ureg("hp"):
        minimum_shaft_input_power = 1.5
    elif 2.0 * ureg("hp") <= shaft_input_power < 5.0 * ureg("hp"):
        minimum_shaft_input_power = 2.0
    elif 3.0 * ureg("hp") <= shaft_input_power < 7.5 * ureg("hp"):
        minimum_shaft_input_power = 3.0
    elif 5.0 * ureg("hp") <= shaft_input_power < 7.5 * ureg("hp"):
        minimum_shaft_input_power = 5.0
    elif 7.5 * ureg("hp") <= shaft_input_power < 10.0 * ureg("hp"):
        minimum_shaft_input_power = 7.5
    elif 10.0 * ureg("hp") <= shaft_input_power < 15.0 * ureg("hp"):
        minimum_shaft_input_power = 10.0
    elif 15.0 * ureg("hp") <= shaft_input_power < 20.0 * ureg("hp"):
        minimum_shaft_input_power = 15.0
    elif 20.0 * ureg("hp") <= shaft_input_power < 25.0 * ureg("hp"):
        minimum_shaft_input_power = 20.0
    elif 25.0 * ureg("hp") <= shaft_input_power < 30.0 * ureg("hp"):
        minimum_shaft_input_power = 25.0
    elif 30.0 * ureg("hp") <= shaft_input_power < 40.0 * ureg("hp"):
        minimum_shaft_input_power = 30.0
    elif 40.0 * ureg("hp") <= shaft_input_power < 50.0 * ureg("hp"):
        minimum_shaft_input_power = 40.0
    elif 50.0 * ureg("hp") <= shaft_input_power < 60.0 * ureg("hp"):
        minimum_shaft_input_power = 50.0
    elif 60.0 * ureg("hp") <= shaft_input_power < 75.0 * ureg("hp"):
        minimum_shaft_input_power = 60.0
    elif 75.0 * ureg("hp") <= shaft_input_power < 100.0 * ureg("hp"):
        minimum_shaft_input_power = 75.0
    elif 100.0 * ureg("hp") <= shaft_input_power < 125.0 * ureg("hp"):
        minimum_shaft_input_power = 100.0
    elif 125.0 * ureg("hp") <= shaft_input_power < 150.0 * ureg("hp"):
        minimum_shaft_input_power = 125.0
    elif 150.0 * ureg("hp") <= shaft_input_power < 200.0 * ureg("hp"):
        minimum_shaft_input_power = 150.0
    elif 200.0 * ureg("hp") <= shaft_input_power:
        minimum_shaft_input_power = 200.0

    nominal_full_load_efficiency = find_osstd_table_entry(
        [("minimum_capacity", minimum_shaft_input_power)],
        osstd_table=data["ashrae_90_1_prm_2019.motors"],
    )["nominal_full_load_efficiency"]

    return {"nominal_full_load_efficiency": nominal_full_load_efficiency}
