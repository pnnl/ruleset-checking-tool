import pytest

from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type
from rct229.schema.config import ureg

# Constants
from rct229.utils.assertions import MissingKeyException

DEGREES = ureg("degrees")

TEST_SURFACES = {
    "ABOVE-GRADE WALL": {
        "adjacent_to": "INTERIOR",
        "construction": {"has_radiant_heating": False},
        "tilt": 80 * DEGREES,
    },
    "BELOW-GRADE WALL": {
        "adjacent_to": "GROUND",
        "construction": {"has_radiant_heating": True},
        "tilt": 100 * DEGREES,
    },
    "FLOOR": {
        "adjacent_to": "EXTERIOR",
        "construction": {"has_radiant_heating": False},
        "tilt": 160 * DEGREES,
    },
    "HEATED SLAB-ON-GRADE": {
        "adjacent_to": "GROUND",
        "construction": {"has_radiant_heating": True},
        "tilt": 120 * DEGREES,
    },
    "ROOF": {
        "adjacent_to": "EXTERIOR",
        "construction": {"has_radiant_heating": False},
        "tilt": 30 * DEGREES,
    },
    "UNHEATED SLAB-ON-GRADE": {
        "adjacent_to": "GROUND",
        "construction": {"has_radiant_heating": False},
        "tilt": 180 * DEGREES,
    },
}

MISS_KEY_SURFACE = {
    "ABOVE-GRADE WALL": {
        "id": "surface",
        "adjacent_to": "INTERIOR",
        "construction": {"has_radiant_heating": False},
    },
}


def test__get_opaque_surface_type_raise_exception():
    try:
        get_opaque_surface_type(MISS_KEY_SURFACE["ABOVE-GRADE WALL"])
    except MissingKeyException as ke:
        assert str(ke) == "$:surface is missing tilt field"


def test__get_opaque_surface_type():
    for key in TEST_SURFACES:
        assert get_opaque_surface_type(TEST_SURFACES[key]) == key, f"Failed {key} test"
