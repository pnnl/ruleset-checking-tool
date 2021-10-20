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


def test__table_G34_CZ1A_ABOVE_GRADE_WALL_EXTERIOR_NON_RESIDENTIAL():
    assert table_G34_lookup("CZ1A", "EXTERIOR NON-RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.124
    }


def test__table_G34_CZ2A_ABOVE_GRADE_WALL_SEMI_EXTERIOR():
    assert table_G34_lookup("CZ2A", "SEMI-EXTERIOR", "ABOVE-GRADE WALL") == {
        "u_value": 0.352
    }


def test__table_G34_CZ3A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ3A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.124
    }


def test__table_G34_CZ3A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ3A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.084
    }


def test__table_G34_CZ4A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ4A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.064
    }


def test__table_G34_CZ5A_ABOVE_GRADE_WALL_SEMI_EXTERIOR():
    assert table_G34_lookup("CZ5A", "SEMI-EXTERIOR", "ABOVE-GRADE WALL") == {
        "u_value": 0.124
    }


def test__table_G34_CZ6A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ6A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.064
    }


def test__table_G34_CZ7_ABOVE_GRADE_WALL_NON_RESIDENTIAL():
    assert table_G34_lookup("CZ7", "EXTERIOR NON-RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.064
    }


def test__table_CZ8_CZ0A_ABOVE_GRADE_WALL_SEMI_EXTERIOR():
    assert table_G34_lookup("CZ8", "SEMI-EXTERIOR", "ABOVE-GRADE WALL") == {
        "u_value": 0.124
    }
