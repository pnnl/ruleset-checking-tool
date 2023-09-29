from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_9_5_1_fns import (
    lighting_space_type_enumeration_to_lpd_map,
    table_9_5_1_lookup,
)
from rct229.rulesets.ashrae9012019.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
)
from rct229.schema.config import ureg

watts_per_ft2 = ureg("watt / foot**2")


# Testing table_9_5_1------------------------------------------
def test__table_9_5_1__gymnasium():
    assert table_9_5_1_lookup("GYMNASIUM") == {"lpd": 0.76 * watts_per_ft2}


def test__table_9_5_1_dormitory():
    assert table_9_5_1_lookup("HOSPITAL") == {"lpd": 0.96 * watts_per_ft2}


# Testing lighting_space_type_enumeration_to_lpd_map ----------
def test__lighting_space_type_enumeration_to_lpd_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="building_area_type",
        enum_type="LightingBuildingAreaOptions2019ASHRAE901T951TG38",
        osstd_table=data["ashrae_90_1_table_9_5_1"],
        enumeration_to_match_field_value_map=lighting_space_type_enumeration_to_lpd_map,
        exclude_enum_names=["NONE"],
    )
