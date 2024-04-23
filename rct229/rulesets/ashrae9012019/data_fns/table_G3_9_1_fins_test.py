from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_1_fins import table_G3_9_1_lookup
from rct229.schema.config import ureg


def test__table_G3_9_lookup__1_shaft_input_power():
    assert table_G3_9_1_lookup(
        shaft_input_power=0.5 * ureg("hp"),
    ) == {"nominal_full_load_efficiency": 0.825}


def test__table_G3_9_lookup__7_5_shaft_input_power():
    assert table_G3_9_1_lookup(
        shaft_input_power=7.5 * ureg("hp"),
    ) == {"nominal_full_load_efficiency": 0.895}


def test__table_G3_9_lookup__50_shaft_input_power():
    assert table_G3_9_1_lookup(
        shaft_input_power=50.0 * ureg("hp"),
    ) == {"nominal_full_load_efficiency": 0.93}
