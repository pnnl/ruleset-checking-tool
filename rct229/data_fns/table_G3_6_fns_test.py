import pytest

from rct229.data import data
from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_6_fns import (
    building_exterior_enumeration_to_lpd_space_type_map,
    table_G3_6_lookup,
)
from rct229.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
    find_osstd_table_entry,
)
from rct229.schema.config import ureg

watts_per_ft2 = ureg("watt / foot**2")
watts_per_linear_ft = ureg("watt / foot")


# Testing table_G3_6------------------------------------------
def test__table_G3_6_UNCOVERED_PARKING_LOTS_AND_DRIVES():
    assert table_G3_6_lookup("UNCOVERED_PARKING_LOTS_AND_DRIVES") == {"lpd": 0.15 * watts_per_ft2, "linear_lpd": None}

def test__table_G3_6_WALKWAY_NARROW():
    assert table_G3_6_lookup("WALKWAY_NARROW") == {"lpd": None, "linear_lpd": 1.0 * watts_per_linear_ft}

def test__table_G3_6_WALKWAY_WIDE():
    assert table_G3_6_lookup("WALKWAY_WIDE") == {"lpd": 0.2 * watts_per_ft2, "linear_lpd": None}

def test__table_G3_6_PLAZA_AREAS():
    assert table_G3_6_lookup("PLAZA_AREAS") == {"lpd": 0.2 * watts_per_ft2, "linear_lpd": None}

def test__table_G3_6_SPECIAL_FEATURE_AREAS():
    assert table_G3_6_lookup("SPECIAL_FEATURE_AREAS") == {"lpd": 0.2 * watts_per_ft2, "linear_lpd": None}

def test__table_G3_6_STAIRWAYS():
    assert table_G3_6_lookup("STAIRWAYS") == {"lpd": 1.0 * watts_per_ft2, "linear_lpd": None}

def test__table_G3_6_MAIN_ENTRANCE_DOOR():
    assert table_G3_6_lookup("MAIN_ENTRANCE_DOOR") == {"lpd": None, "linear_lpd": 30.0 * watts_per_linear_ft}

def test__table_G3_6_OTHER_ENTRANCE_OR_EXIT_DOORS():
    assert table_G3_6_lookup("OTHER_ENTRANCE_OR_EXIT_DOORS") == {"lpd": None, "linear_lpd": 20.0 * watts_per_linear_ft}

def test__table_G3_6_EXTERIOR_CANOPIES():
    assert table_G3_6_lookup("EXTERIOR_CANOPIES") == {"lpd": 1.25 * watts_per_ft2, "linear_lpd": None}

def test__table_G3_6_OUTDOOR_SALES_OPEN_AREAS():
    assert table_G3_6_lookup("OUTDOOR_SALES_OPEN_AREAS") == {"lpd": 0.5 * watts_per_ft2, "linear_lpd": None}

def test__table_G3_6_STREET_FRONTAGE():
    assert table_G3_6_lookup("STREET_FRONTAGE") == {"lpd": None , "linear_lpd": 20.0 * watts_per_linear_ft}

def test__table_G3_6_NON_TRADABLE_FACADE():
    assert table_G3_6_lookup("NON_TRADABLE_FACADE") == {"lpd": 0.2 * watts_per_ft2, "linear_lpd": 5.0 * watts_per_linear_ft}

# Testing building_exterior_enumeration_to_lpd_space_type_map ----------
def test__building_exterior_enumeration_to_lpd_space_type_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="building_exterior_type",
        enum_type="ExteriorLightingAreas2019ASHRAE901TableG36",
        osstd_table=data["ashrae_90_1_table_3_6"],
        enumeration_to_match_field_value_map=building_exterior_enumeration_to_lpd_space_type_map,
    )
