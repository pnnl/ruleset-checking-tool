import pytest

from rct229.data import data
from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_3_2_fns import (
    climate_zone_enumeration_to_climate_zone_type_map,
    table_3_2_lookup,
)
from rct229.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
    find_osstd_table_entry,
)


# Testing table_3_2------------------------------------------
def test__table_3_2_CZ0():
    assert table_3_2_lookup("CZ0B") == {"system_min_heating_output": 5}

def test__table_3_2_CZ1():
    assert table_3_2_lookup("CZ1A") == {"system_min_heating_output": 5}

def test__table_3_2_CZ2():
    assert table_3_2_lookup("CZ2A") == {"system_min_heating_output": 5}

def test__table_3_2_CZ3():
    assert table_3_2_lookup("CZ3A") == {"system_min_heating_output": 9}

def test__table_3_2_CZ4():
    assert table_3_2_lookup("CZ4A") == {"system_min_heating_output": 10}

def test__table_3_2_CZ5():
    assert table_3_2_lookup("CZ5A") == {"system_min_heating_output": 12}

def test__table_3_2_CZ6():
    assert table_3_2_lookup("CZ6A") == {"system_min_heating_output": 14}

def test__table_3_2_CZ7():
    assert table_3_2_lookup("CZ7") == {"system_min_heating_output": 16}

def test__table_3_2_CZ8():
    assert table_3_2_lookup("CZ8") == {"system_min_heating_output": 19}
    
# Testing climate_zone_enumeration_to_climate_zone_type_map ----------
def test__lighting_space_enumeration_to_lpd_space_type_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="climate_zone",
        enum_type="ClimateZone2019ASHRAE901",
        osstd_table=data["ashrae_90_1_table_3_2"],
        enumeration_to_match_field_value_map=climate_zone_enumeration_to_climate_zone_type_map
    )
