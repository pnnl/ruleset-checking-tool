from rct229.rulesets.ashrae9012019.data_fns.table_G3_1_1_2_fns import (
    table_g3_1_2_lookup,
)


def test__table_g3_1_2_lookup__Courthouse():
    assert table_g3_1_2_lookup("COURTHOUSE") == {
        "baseline_heating_method": "ELECTRIC_RESISTANCE_STORAGE_WATER_HEATER"
    }


def test__table_g3_1_2_lookup__Fire_station():
    assert table_g3_1_2_lookup("FIRE_STATION") == {
        "baseline_heating_method": "GAS_STORAGE_WATER_HEATER"
    }


def test__table_g3_1_2_lookup__Hospital_and_outpatient_surgery_center():
    assert table_g3_1_2_lookup("HOSPITAL_AND_OUTPATIENT_SURGERY") == {
        "baseline_heating_method": "GAS_STORAGE_WATER_HEATER"
    }


def test__table_g3_1_2_lookup__Motel():
    assert table_g3_1_2_lookup("MOTEL") == {
        "baseline_heating_method": "GAS_STORAGE_WATER_HEATER"
    }


def test__table_g3_1_2_lookup__Museum():
    assert table_g3_1_2_lookup("MUSEUM") == {
        "baseline_heating_method": "ELECTRIC_RESISTANCE_STORAGE_WATER_HEATER"
    }


def test__table_g3_1_2_lookup__Post_office():
    assert table_g3_1_2_lookup("POST_OFFICE") == {
        "baseline_heating_method": "ELECTRIC_RESISTANCE_STORAGE_WATER_HEATER"
    }


def test__table_g3_1_2_lookup__School_university():
    assert table_g3_1_2_lookup("SCHOOL_UNIVERSITY") == {
        "baseline_heating_method": "GAS_STORAGE_WATER_HEATER"
    }


def test__table_g3_1_2_lookup__Warehouse():
    assert table_g3_1_2_lookup("WAREHOUSE") == {
        "baseline_heating_method": "ELECTRIC_RESISTANCE_STORAGE_WATER_HEATER"
    }
