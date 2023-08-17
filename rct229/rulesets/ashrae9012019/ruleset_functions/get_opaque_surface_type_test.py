from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.schema.config import ureg

# Constants
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


def test__get_opaque_surface_type():
    for key in TEST_SURFACES:
        assert get_opaque_surface_type(TEST_SURFACES[key]) == key, f"Failed {key} test"
