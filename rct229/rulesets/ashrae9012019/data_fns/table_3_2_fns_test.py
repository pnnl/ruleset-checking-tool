from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_3_2_fns import (
    table_3_2_climate_zone_enumeration_to_climate_zone_map,
    table_3_2_lookup,
)
from rct229.rulesets.ashrae9012019.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
)
from rct229.schema.config import ureg

btuh_per_ft2 = ureg("british_thermal_unit / (hour * foot ** 2)")


# Testing table_3_2------------------------------------------
def test__table_3_2_CZ0():
    assert table_3_2_lookup("CZ0B") == {"system_min_heating_output": 5 * btuh_per_ft2}


def test__table_3_2_CZ1():
    assert table_3_2_lookup("CZ1A") == {"system_min_heating_output": 5 * btuh_per_ft2}


def test__table_3_2_CZ2():
    assert table_3_2_lookup("CZ2A") == {"system_min_heating_output": 5 * btuh_per_ft2}


def test__table_3_2_CZ3():
    assert table_3_2_lookup("CZ3A") == {"system_min_heating_output": 9 * btuh_per_ft2}


def test__table_3_2_CZ4():
    assert table_3_2_lookup("CZ4A") == {"system_min_heating_output": 10 * btuh_per_ft2}


def test__table_3_2_CZ5():
    assert table_3_2_lookup("CZ5A") == {"system_min_heating_output": 12 * btuh_per_ft2}


def test__table_3_2_CZ6():
    assert table_3_2_lookup("CZ6A") == {"system_min_heating_output": 14 * btuh_per_ft2}


def test__table_3_2_CZ7():
    assert table_3_2_lookup("CZ7") == {"system_min_heating_output": 16 * btuh_per_ft2}


def test__table_3_2_CZ8():
    assert table_3_2_lookup("CZ8") == {"system_min_heating_output": 19 * btuh_per_ft2}


# Testing climate_zone_enumeration_to_climate_zone_map ----------
def test__climate_zone_enumeration_to_climate_zone_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="climate_zone",
        enum_type="ClimateZoneOptions2019ASHRAE901",
        osstd_table=data["ashrae_90_1_table_3_2"],
        enumeration_to_match_field_value_map=table_3_2_climate_zone_enumeration_to_climate_zone_map,
    )
