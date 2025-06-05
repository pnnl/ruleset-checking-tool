from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_G3_8_fns import (
    lighting_space_enumeration_to_lpd_space_type_map,
    table_G3_8_lookup,
)
from rct229.rulesets.ashrae9012019.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
)
from rct229.schema.config import ureg

watts_per_ft2 = ureg("watt / foot**2")


# Testing table_G3_8_lpd() ------------------------------------------
def test__table_G3_8_lpd__automotive_facility():
    assert table_G3_8_lookup("AUTOMOTIVE_FACILITY") == {"lpd": 0.9 * watts_per_ft2}


def test__table_G3_8_lpd__convention_center():
    assert table_G3_8_lookup("CONVENTION_CENTER") == {"lpd": 1.20 * watts_per_ft2}


def test_t_able_G3_8_lpd__courthouse():
    assert table_G3_8_lookup("COURTHOUSE") == {"lpd": 1.20 * watts_per_ft2}


def test__table_G3_8_lpd__workshop():
    assert table_G3_8_lookup("WORKSHOP") == {"lpd": 1.40 * watts_per_ft2}


def test__table_G3_8_lpd__warehouse():
    assert table_G3_8_lookup("WAREHOUSE") == {"lpd": 0.80 * watts_per_ft2}


def test__table_G3_8_lpd__courthouse():
    assert table_G3_8_lookup("COURTHOUSE") == {"lpd": 1.20 * watts_per_ft2}


# Testing lighting_space_enumeration_to_lpd_space_type_map ----------
def test__lighting_space_enumeration_to_lpd_space_type_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="lpd_space_type",
        enum_type="LightingBuildingAreaOptions2019ASHRAE901T951TG38",
        osstd_table=data["ashrae_90_1_prm_2019.prm_interior_lighting"],
        enumeration_to_match_field_value_map=lighting_space_enumeration_to_lpd_space_type_map,
        exclude_enum_names=["NONE"],
    )
