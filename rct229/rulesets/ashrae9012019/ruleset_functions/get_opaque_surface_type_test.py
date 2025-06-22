from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.schema.config import ureg

# Constants
DEGREES = ureg("degrees")

TEST_SURFACES = {
    "ABOVE-GRADE WALL": {
        "adjacent_to": "INTERIOR",
        "construction": "sample_construction",
        "tilt": 80 * DEGREES,
    },
    "BELOW-GRADE WALL": {
        "adjacent_to": "GROUND",
        "construction": "sample_construction",
        "tilt": 100 * DEGREES,
    },
    "FLOOR": {
        "adjacent_to": "EXTERIOR",
        "construction": "sample_construction",
        "tilt": 160 * DEGREES,
    },
    "HEATED SLAB-ON-GRADE": {
        "adjacent_to": "GROUND",
        "construction": "sample_construction",
        "tilt": 120 * DEGREES,
    },
    "ROOF": {
        "adjacent_to": "EXTERIOR",
        "construction": "sample_construction",
        "tilt": 30 * DEGREES,
    },
    "UNHEATED SLAB-ON-GRADE": {
        "adjacent_to": "GROUND",
        "construction": "unheated_sample_construction",
        "tilt": 180 * DEGREES,
    },
}

constructions = [
    {"id": "sample_construction", "has_radiant_heating": True},
    {"id": "unheated_sample_construction", "has_radiant_heating": False},
]


def test__get_opaque_surface_type():
    for key in TEST_SURFACES:
        assert (
            get_opaque_surface_type(TEST_SURFACES[key], constructions) == key
        ), f"Failed {key} test"
