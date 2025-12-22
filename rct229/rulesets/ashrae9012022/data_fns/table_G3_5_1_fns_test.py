from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_1_fns import table_g3_5_1_lookup


# Testing table_3_5_1------------------------------------------
def test__table_3_5_1_ac_0():
    assert table_g3_5_1_lookup(0) == {
        "minimum_efficiency": 3.0,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.6,
    }


def test__table_3_5_1_ac_64999():
    assert table_g3_5_1_lookup(64999) == {
        "minimum_efficiency": 3.0,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.6,
    }


def test__table_3_5_1_ac_65000():
    assert table_g3_5_1_lookup(65000) == {
        "minimum_efficiency": 3.5,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.6,
    }


def test__table_3_5_1_ac_180000():
    assert table_g3_5_1_lookup(180000) == {
        "minimum_efficiency": 3.4,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.6,
    }


def test__table_3_5_1_ac_360000():
    assert table_g3_5_1_lookup(360000) == {
        "minimum_efficiency": 3.5,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.6,
    }


def test__table_3_5_1_ac_1000000():
    assert table_g3_5_1_lookup(1000000) == {
        "minimum_efficiency": 3.6,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.6,
    }
