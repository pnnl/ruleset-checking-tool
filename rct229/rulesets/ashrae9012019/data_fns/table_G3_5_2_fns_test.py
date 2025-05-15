from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_2_fns import (
    HeatPumpEquipmentType,
    RatingCondition,
    table_g3_5_2_lookup,
)


# Testing table_3_5_2------------------------------------------
def test__table_3_5_2_cooling_0():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_COOLING,
        RatingCondition.SINGLE_PACKAGE,
        0,
    ) == {
        "minimum_efficiency": 3.0,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.4,
    }


def test__table_3_5_2_cooling_64999():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_COOLING,
        RatingCondition.SINGLE_PACKAGE,
        64999,
    ) == {
        "minimum_efficiency": 3.0,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.4,
    }


def test__table_3_5_2_cooling_65000():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_COOLING,
        RatingCondition.SINGLE_PACKAGE,
        65000,
    ) == {
        "minimum_efficiency": 3.4,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.4,
    }


def test__table_3_5_2_cooling_135000():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_COOLING,
        RatingCondition.SINGLE_PACKAGE,
        180000,
    ) == {
        "minimum_efficiency": 3.2,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.4,
    }


def test__table_3_5_2_cooling_240000():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_COOLING,
        RatingCondition.SINGLE_PACKAGE,
        360000,
    ) == {
        "minimum_efficiency": 3.1,
        "efficiency_metric": "FULL_LOAD_COEFFICIENT_OF_PERFORMANCE_NO_FAN",
        "most_conservative_efficiency": 3.4,
    }


def test__table_3_5_2_heating_pkg_0():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
        RatingCondition.SINGLE_PACKAGE,
        0,
    ) == {
        "minimum_efficiency": 3.4,
        "efficiency_metric": "HEAT_PUMP_COEFFICIENT_OF_PERFORMANCE_HIGH_TEMPERATURE_NO_FAN",
        "most_conservative_efficiency": 3.4,
    }


def test__table_3_5_2_heating_pkg_64999():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
        RatingCondition.SINGLE_PACKAGE,
        64999,
    ) == {
        "minimum_efficiency": 3.4,
        "efficiency_metric": "HEAT_PUMP_COEFFICIENT_OF_PERFORMANCE_HIGH_TEMPERATURE_NO_FAN",
        "most_conservative_efficiency": 3.4,
    }


def test__table_3_5_2_heating_47_65000():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
        RatingCondition.HIGH_TEMP,
        65000,
    ) == {
        "minimum_efficiency": 3.4,
        "efficiency_metric": "HEAT_PUMP_COEFFICIENT_OF_PERFORMANCE_HIGH_TEMPERATURE_NO_FAN",
        "most_conservative_efficiency": 3.4,
    }


def test__table_3_5_2_heating_17_65000():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
        RatingCondition.LOW_TEMP,
        65000,
    ) == {
        "minimum_efficiency": 2.3,
        "efficiency_metric": "HEAT_PUMP_COEFFICIENT_OF_PERFORMANCE_LOW_TEMPERATURE_NO_FAN",
        "most_conservative_efficiency": 2.3,
    }


def test__table_3_5_2_heating_47_135000():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
        RatingCondition.HIGH_TEMP,
        135000,
    ) == {
        "minimum_efficiency": 3.4,
        "efficiency_metric": "HEAT_PUMP_COEFFICIENT_OF_PERFORMANCE_HIGH_TEMPERATURE_NO_FAN",
        "most_conservative_efficiency": 3.4,
    }


def test__table_3_5_2_heating_17_135000():
    assert table_g3_5_2_lookup(
        HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
        RatingCondition.LOW_TEMP,
        135000,
    ) == {
        "minimum_efficiency": 2.1,
        "efficiency_metric": "HEAT_PUMP_COEFFICIENT_OF_PERFORMANCE_LOW_TEMPERATURE_NO_FAN",
        "most_conservative_efficiency": 2.3,
    }
