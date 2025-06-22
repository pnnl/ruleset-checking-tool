from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.schema.config import ureg

# Constants
DEGREES = ureg("degrees")

CONSTRUCTIONS = [
    {
        "id": "Heated",
        "has_radiant_heating": True,
    },
    {
        "id": "Unheated",
        "has_radiant_heating": False,
    },
]
TEST_SURFACES = {
    "ABOVE-GRADE WALL": {
        "adjacent_to": "INTERIOR",
        "construction": "Unheated",
        "tilt": 80 * DEGREES,
    },
    "BELOW-GRADE WALL": {
        "adjacent_to": "GROUND",
        "construction": "Heated",
        "tilt": 100 * DEGREES,
    },
    "FLOOR": {
        "adjacent_to": "EXTERIOR",
        "construction": "Unheated",
        "tilt": 160 * DEGREES,
    },
    "HEATED SLAB-ON-GRADE": {
        "adjacent_to": "GROUND",
        "construction": "Heated",
        "tilt": 120 * DEGREES,
    },
    "ROOF": {
        "adjacent_to": "EXTERIOR",
        "construction": "Unheated",
        "tilt": 30 * DEGREES,
    },
    "UNHEATED SLAB-ON-GRADE": {
        "adjacent_to": "GROUND",
        "construction": "Unheated",
        "tilt": 180 * DEGREES,
    },
}

constructions = [
    {"id": "sample_construction", "has_radiant_heating": True},
    {"id": "unheated_sample_construction", "has_radiant_heating": False},
]


def test__get_opaque_surface_type():
    for key in TEST_SURFACES:
        construction = next(
            (c for c in CONSTRUCTIONS if c["id"] == TEST_SURFACES[key]["construction"]),
        )
        has_radiant_heating = construction.get("has_radiant_heating", False)
        assert (
            get_opaque_surface_type(TEST_SURFACES[key], has_radiant_heating) == key
        ), f"Failed {key} test"
