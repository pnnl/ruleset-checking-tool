from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_4_fns import (
    EquipmentType,
    table_g3_5_4_lookup,
)


# Testing table_3_5_4------------------------------------------
def test__table_3_5_4_ptac():
    assert table_g3_5_4_lookup(EquipmentType.PTAC_COOLING) == {
        "minimum_efficiency": 3.2,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": None,
    }


def test__table_3_5_4_pthp_cooling():
    assert table_g3_5_4_lookup(EquipmentType.PTHP_COOLING) == {
        "minimum_efficiency": 3.1,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": None,
    }


def test__table_3_5_4_pthp_heating():
    assert table_g3_5_4_lookup(EquipmentType.PTHP_HEATING) == {
        "minimum_efficiency": 3.1,
        "efficiency_metric": "HEAT_PUMP_EFFICIENCY_HIGH_TEMPERATURE_NO_FAN",
        "most_conservative_efficiency": None,
    }
