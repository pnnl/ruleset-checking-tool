from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_3_fins import table_G3_9_3_lookup
from rct229.schema.config import ureg


def test__table_G3_9_lookup__15_hp_shaft_power():
    assert table_G3_9_3_lookup(
        shaft_input_power=15.0 * ureg("hp"),
    ) == {"full_load_motor_efficiency_for_modeling": 0.75}


def test__table_G3_9_lookup__25_hp_shaft_power():
    assert table_G3_9_3_lookup(
        shaft_input_power=25.0 * ureg("hp"),
    ) == {"full_load_motor_efficiency_for_modeling": 0.78}


def test__table_G3_9_lookup__105_hp_shaft_power():
    assert table_G3_9_3_lookup(
        shaft_input_power=105.0 * ureg("hp"),
    ) == {"full_load_motor_efficiency_for_modeling": 0.80}
