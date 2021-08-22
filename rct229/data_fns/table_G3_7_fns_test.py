import pytest
from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_7_fns import (
    _osstd_prm_interior_lighting_data,
    lighting_space_enumeration_to_lpd_space_type_map,
    table_G3_7_lpd,
)
from rct229.data_fns.table_utils import find_osstd_table_entry


# Testing table_G3_7_lpd()
def test__table_G3_7_lpd__with_w_per_ft_null():
    assert (
        table_G3_7_lpd(lighting_space_type="DORMITORY_LIVING_QUARTERS", space_height=8)
        == 1.11
    )


def test__table_G3_7_lpd__with_w_per_ft_null():
    assert (
        table_G3_7_lpd(lighting_space_type="ATRIUM_HIGH", space_height=20)
        == 0.5 + 0.025 * 20
    )


# Testing lighting_space_enumeration_to_lpd_space_type_map
def test__lighting_space_enumeration_to_lpd_space_type_map():
    lighting_space_type_enum = schema_enums["LightingSpaceType2019ASHRAE901TG37"]
    for e_lighting_space_type in lighting_space_type_enum:
        lighting_space_type = e_lighting_space_type.name

        # Make sure each space type in the enumeration is in our map
        lpd_space_type = lighting_space_enumeration_to_lpd_space_type_map[
            lighting_space_type
        ]
        assert lpd_space_type is not None

        # Make sure there is a corresponding entry in the OSSTD table
        # find_osstd_table_entry() will throw if not
        entry = find_osstd_table_entry(
            match_field_value=lpd_space_type,
            match_field_name="lpd_space_type",
            osstd_table=_osstd_prm_interior_lighting_data,
        )
