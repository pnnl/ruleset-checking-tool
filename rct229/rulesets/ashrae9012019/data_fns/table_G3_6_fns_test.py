from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_G3_6_fns import (
    EXTERIOR_LIGHTING_AREA_ENUMERATION_TO_BUILDING_EXTERIOR_TYPE_MAP,
    table_G3_6_lookup,
)
from rct229.rulesets.ashrae9012019.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
)
from rct229.schema.config import ureg

WATTS_PER_FT2 = ureg("watt / foot**2")
WATTS_PER_LINEAR_FT = ureg("watt / foot")
WATT_PER_LOCATION = ureg("watt")
WATT_PER_DEVICE = ureg("watt")


# Testing table_G3_6------------------------------------------
def test__table_G3_6_UNCOVERED_PARKING_LOTS_AND_DRIVES():
    assert table_G3_6_lookup("UNCOVERED_PARKING_LOTS_AND_DRIVES") == {
        "lpd": 0.15 * WATTS_PER_FT2,
        "linear_lpd": None,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_WALKWAY_NARROW():
    assert table_G3_6_lookup("WALKWAY_NARROW") == {
        "lpd": None,
        "linear_lpd": 1.0 * WATTS_PER_LINEAR_FT,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_WALKWAY_WIDE():
    assert table_G3_6_lookup("WALKWAY_WIDE") == {
        "lpd": 0.2 * WATTS_PER_FT2,
        "linear_lpd": None,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_PLAZA_AREAS():
    assert table_G3_6_lookup("PLAZA_AREAS") == {
        "lpd": 0.2 * WATTS_PER_FT2,
        "linear_lpd": None,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_SPECIAL_FEATURE_AREAS():
    assert table_G3_6_lookup("SPECIAL_FEATURE_AREAS") == {
        "lpd": 0.2 * WATTS_PER_FT2,
        "linear_lpd": None,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_STAIRWAYS():
    assert table_G3_6_lookup("STAIRWAYS") == {
        "lpd": 1.0 * WATTS_PER_FT2,
        "linear_lpd": None,
        "device_lpd": None,
        "location_lpd": None,
    }


def test__table_G3_6_MAIN_ENTRANCE_DOOR():
    assert table_G3_6_lookup("MAIN_ENTRANCE_DOOR") == {
        "lpd": None,
        "linear_lpd": 30.0 * WATTS_PER_LINEAR_FT,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_OTHER_ENTRANCE_OR_EXIT_DOORS():
    assert table_G3_6_lookup("OTHER_ENTRANCE_OR_EXIT_DOORS") == {
        "lpd": None,
        "linear_lpd": 20.0 * WATTS_PER_LINEAR_FT,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_EXTERIOR_CANOPIES():
    assert table_G3_6_lookup("EXTERIOR_CANOPIES") == {
        "lpd": 1.25 * WATTS_PER_FT2,
        "linear_lpd": None,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_OUTDOOR_SALES_OPEN_AREAS():
    assert table_G3_6_lookup("OUTDOOR_SALES_OPEN_AREAS") == {
        "lpd": 0.5 * WATTS_PER_FT2,
        "linear_lpd": None,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_STREET_FRONTAGE():
    assert table_G3_6_lookup("STREET_FRONTAGE") == {
        "lpd": None,
        "linear_lpd": 20.0 * WATTS_PER_LINEAR_FT,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_EMERGENCY_VEHICLE_LOADING_AREA():
    assert table_G3_6_lookup("EMERGENCY_VEHICLE_LOADING_AREA") == {
        "lpd": 0.5 * WATTS_PER_FT2,
        "linear_lpd": None,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_DRIVE_UP_WINDOWS_FAST_FOOD():
    assert table_G3_6_lookup("DRIVE_UP_WINDOWS_FAST_FOOD") == {
        "lpd": None,
        "linear_lpd": None,
        "location_lpd": 400 * WATT_PER_LOCATION,
        "device_lpd": None,
    }


def test__table_G3_6_PARKING_NEAR_24HR_RETAIL_ENTRANCES():
    assert table_G3_6_lookup("PARKING_NEAR_24HR_RETAIL_ENTRANCES") == {
        "lpd": None,
        "linear_lpd": None,
        "location_lpd": 800 * WATT_PER_LOCATION,
        "device_lpd": None,
    }


def test__table_G3_6_BUILDING_FACADE():
    assert table_G3_6_lookup("BUILDING_FACADE") == {
        "lpd": 0.2 * WATTS_PER_FT2,
        "linear_lpd": 5.0 * WATTS_PER_LINEAR_FT,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_ENTRANCE_AND_GATEHOUSE():
    assert table_G3_6_lookup("ENTRANCE_AND_GATEHOUSE") == {
        "lpd": 1.25 * WATTS_PER_FT2,
        "linear_lpd": None,
        "location_lpd": None,
        "device_lpd": None,
    }


def test__table_G3_6_AUTOMATED_TELLER_MACHINES():
    assert table_G3_6_lookup("AUTOMATED_TELLER_MACHINES") == {
        "lpd": None,
        "linear_lpd": None,
        "location_lpd": 270 * WATT_PER_LOCATION,
        "device_lpd": 90 * WATT_PER_DEVICE,
    }


def test__table_G3_6_NIGHT_DEPOSITORIES():
    assert table_G3_6_lookup("NIGHT_DEPOSITORIES") == {
        "lpd": None,
        "linear_lpd": None,
        "location_lpd": 270 * WATT_PER_LOCATION,
        "device_lpd": 90 * WATT_PER_DEVICE,
    }


# Testing exterior_lighting_area_enumeration_to_building_exterior_type_map ----------
def test__exterior_lighting_area_enumeration_to_building_exterior_type_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="building_exterior_type",
        enum_type="ExteriorLightingAreaOptions2019ASHRAE901TableG36",
        osstd_table=data["ashrae_90_1_table_G3_6"],
        enumeration_to_match_field_value_map=EXTERIOR_LIGHTING_AREA_ENUMERATION_TO_BUILDING_EXTERIOR_TYPE_MAP,
        exclude_enum_names=["MISCELLANEOUS_TRADABLE", "MISCELLANEOUS_NON_TRADABLE"],
    )
