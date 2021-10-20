import pytest

from rct229.data import data
from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_4_fns import (
    CLIMATE_ZONE_ENUMERATION_TO_CLIMATE_ZONE_MAP,
    OPAQUE_SURFACE_TYPE_TO_CONSTRUCTION_MAP,
    SURFACE_CONDITIONING_CATEGORY_TO_BUILDING_CATEGORY_MAP,
    table_G34_lookup,
)


def test__table_G34_CZ0A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ0A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.124
    }
