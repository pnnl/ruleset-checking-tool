from rct229.rulesets.ashrae9012019.data_fns.table_G3_1_1_2_fns import (
    table_g3_1_2_lookup,
)


def test__table_g3_1_2_lookup__Courthouse():
    assert table_g3_1_2_lookup("Courthouse") == {
        "baseline_heating_method": "Electric resistance storage water heater"
    }


def test__table_g3_1_2_lookup__Fire_station():
    assert table_g3_1_2_lookup("Fire station") == {
        "baseline_heating_method": "Gas storage water heater"
    }


def test__table_g3_1_2_lookup__Hospital_and_outpatient_surgery_center():
    assert table_g3_1_2_lookup("Hospital and outpatient surgery center") == {
        "baseline_heating_method": "Gas storage water heater"
    }


def test__table_g3_1_2_lookup__Motel():
    assert table_g3_1_2_lookup("Motel") == {
        "baseline_heating_method": "Gas storage water heater"
    }


def test__table_g3_1_2_lookup__Museum():
    assert table_g3_1_2_lookup("Museum") == {
        "baseline_heating_method": "Electric resistance storage water heater"
    }


def test__table_g3_1_2_lookup__Post_office():
    assert table_g3_1_2_lookup("Post office") == {
        "baseline_heating_method": "Electric resistance storage water heater"
    }


def test__table_g3_1_2_lookup__School_university():
    assert table_g3_1_2_lookup("School/university") == {
        "baseline_heating_method": "Gas storage water heater"
    }


def test__table_g3_1_2_lookup__Warehouse():
    assert table_g3_1_2_lookup("Warehouse") == {
        "baseline_heating_method": "Electric resistance storage water heater"
    }
