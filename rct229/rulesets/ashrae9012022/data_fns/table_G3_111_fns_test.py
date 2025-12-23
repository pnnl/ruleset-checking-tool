from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_G3_111_fns import (
    VERTICAL_FENESTRATION_BUILDING_AREA_TYPE_TO_WWR_BUILDING_TYPE_MAP,
    table_G3_1_1_1_lookup,
)
from rct229.rulesets.ashrae9012019.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
)


# Testing table_G3_1_1_1_lookup() ------------------------------------------
def test__table_G3_1_1_1_GROCERY_STORE():
    assert table_G3_1_1_1_lookup("GROCERY_STORE") == {"wwr": 0.07}


def test__table_G3_1_1_1_HEALTHCARE_OUTPATIENT():
    assert table_G3_1_1_1_lookup("HEALTHCARE_OUTPATIENT") == {"wwr": 0.21}


def test__table_G3_1_1_1_HOSPITAL():
    assert table_G3_1_1_1_lookup("HOSPITAL") == {"wwr": 0.27}


def test__table_G3_1_1_1_HOTEL_MOTEL_SMALL():
    assert table_G3_1_1_1_lookup("HOTEL_MOTEL_SMALL") == {"wwr": 0.24}


def test__table_G3_1_1_1_HOTEL_MOTEL_LARGE():
    assert table_G3_1_1_1_lookup("HOTEL_MOTEL_LARGE") == {"wwr": 0.34}


def test__table_G3_1_1_1_OFFICE_SMALL():
    assert table_G3_1_1_1_lookup("OFFICE_SMALL") == {"wwr": 0.19}


def test__table_G3_1_1_1_OFFICE_MEDIUM():
    assert table_G3_1_1_1_lookup("OFFICE_MEDIUM") == {"wwr": 0.31}


def test__table_G3_1_1_1_OFFICE_LARGE():
    assert table_G3_1_1_1_lookup("OFFICE_LARGE") == {"wwr": 0.40}


def test__table_G3_1_1_1_RESTAURANT_QUICK_SERVICE():
    assert table_G3_1_1_1_lookup("RESTAURANT_QUICK_SERVICE") == {"wwr": 0.34}


def test__table_G3_1_1_1_RESTAURANT_FULL_SERVICE():
    assert table_G3_1_1_1_lookup("RESTAURANT_FULL_SERVICE") == {"wwr": 0.24}


def test__table_G3_1_1_1_RETAIL_STAND_ALONE():
    assert table_G3_1_1_1_lookup("RETAIL_STAND_ALONE") == {"wwr": 0.11}


def test__table_G3_1_1_1_RETAIL_STRIP_MALL():
    assert table_G3_1_1_1_lookup("RETAIL_STRIP_MALL") == {"wwr": 0.20}


def test__table_G3_1_1_1_SCHOOL_PRIMARY():
    assert table_G3_1_1_1_lookup("SCHOOL_PRIMARY") == {"wwr": 0.22}


def test__table_G3_1_1_1_SCHOOL_SECONDARY_AND_UNIVERSITY():
    assert table_G3_1_1_1_lookup("SCHOOL_SECONDARY_AND_UNIVERSITY") == {"wwr": 0.22}


def test__table_G3_1_1_1_WAREHOUSE_NONREFRIGERATED():
    assert table_G3_1_1_1_lookup("WAREHOUSE_NONREFRIGERATED") == {"wwr": 0.06}


# Testing vertical_fenestration_building_area_type_to_wwr_building_type_map()----------
def test__building_area_type_to_vertical_fenestration_percentage_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="wwr_building_type",
        enum_type="VerticalFenestrationBuildingAreaOptions2019ASHRAE901",
        osstd_table=data["ashrae_90_1_prm_2019.prm_wwr_bldg_type"],
        enumeration_to_match_field_value_map=VERTICAL_FENESTRATION_BUILDING_AREA_TYPE_TO_WWR_BUILDING_TYPE_MAP,
    )
