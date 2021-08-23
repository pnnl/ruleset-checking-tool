import pytest
from rct229.data import data
from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_7_fns import (
    lighting_space_enumeration_to_lpd_space_type_map,
    table_G3_7_lpd,
)
from rct229.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
    find_osstd_table_entry,
)


# Testing table_G3_7_lpd() ----------------------------------------
def test__table_G3_7_lpd__with_w_per_ft_null():
    assert (
        table_G3_7_lpd(lighting_space_type="DORMITORY_LIVING_QUARTERS", space_height=8)
        == 1.11
    )


def test__table_G3_7_lpd__with_w_per_ft_not_null():
    assert (
        table_G3_7_lpd(lighting_space_type="ATRIUM_HIGH", space_height=20)
        == 0.5 + 0.025 * 20
    )


# Testing lighting_space_enumeration_to_lpd_space_type_map ----------
def test__lighting_space_enumeration_to_lpd_space_type_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="lpd_space_type",
        enum_type="LightingSpaceType2019ASHRAE901TG37",
        osstd_table=data["ashrae_90_1_prm_2019.prm_interior_lighting"],
        enumeration_to_match_field_value_map=lighting_space_enumeration_to_lpd_space_type_map,
    )
