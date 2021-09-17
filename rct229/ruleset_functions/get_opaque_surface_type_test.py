import pytest
from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type

TEST_SURFACES = {
    "ABOVE-GRADE WALL": {
        "adjacent_to": "INTERIOR",
        "construction": {"has_radiant_heating": False},
        "tilt": 80,
    },
    "BELOW-GRADE WALL": {
        "adjacent_to": "GROUND",
        "construction": {"has_radiant_heating": True},
        "tilt": 100,
    },
    "FLOOR": {
        "adjacent_to": "EXTERIOR",
        "construction": {"has_radiant_heating": False},
        "tilt": 160,
    },
    "HEATED SLAB-ON-GRADE": {
        "adjacent_to": "GROUND",
        "construction": {"has_radiant_heating": True},
        "tilt": 120,
    },
    "ROOF": {
        "adjacent_to": "EXTERIOR",
        "construction": {"has_radiant_heating": False},
        "tilt": 30,
    },
    "UNHEATED SLAB-ON-GRADE": {
        "adjacent_to": "GROUND",
        "construction": {"has_radiant_heating": False},
        "tilt": 180,
    },
}


def test__get_opaque_surface_type():
    for key in TEST_SURFACES:
        assert get_opaque_surface_type(TEST_SURFACES[key]) == key, f"Failed {key} test"
