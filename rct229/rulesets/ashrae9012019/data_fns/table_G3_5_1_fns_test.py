from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_1_fns import table_G3_5_1_lookup
from rct229.schema.config import ureg

btu_h = ureg("btu_h")


# Testing table_3_5_1------------------------------------------
def test__table_3_5_1_ac_60000():
    assert table_G3_5_1_lookup(60000 * btu_h) == {
        "minimum_efficiency": 3.0,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
    }


def test__table_3_5_1_ac_90000():
    assert table_G3_5_1_lookup(90000 * btu_h) == {
        "minimum_efficiency": 3.5,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
    }


def test__table_3_5_1_ac_180000():
    assert table_G3_5_1_lookup(180000 * btu_h) == {
        "minimum_efficiency": 3.4,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
    }


def test__table_3_5_1_ac_360000():
    assert table_G3_5_1_lookup(360000 * btu_h) == {
        "minimum_efficiency": 3.5,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
    }


def test__table_3_5_1_ac_1000000():
    assert table_G3_5_1_lookup(1000000 * btu_h) == {
        "minimum_efficiency": 3.6,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
    }
