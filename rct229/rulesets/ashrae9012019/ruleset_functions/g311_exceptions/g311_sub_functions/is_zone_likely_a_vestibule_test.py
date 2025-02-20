from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_zone_likely_a_vestibule import (
    is_zone_likely_a_vestibule,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "schedules": [{"id": "schedule_1", "hourly_values": [1.2] * 8670}],
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "floor_name": "FLOOR 1",
                            # case has no other data provided - likely not a vestibule
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "floor_area": 1000,
                                },
                                {
                                    "id": "Space 2",
                                    "floor_area": 100,
                                },
                            ],
                        },
                        {
                            # case has door but the space area is greater than 50 or 2% of the floor area
                            "id": "Thermal Zone 2",
                            "floor_name": "FLOOR 1",
                            "spaces": [
                                {
                                    "id": "Space 3",
                                    "floor_area": 1000,
                                },
                            ],
                            "surfaces": [
                                {
                                    "id": "surface 1",
                                    "adjacent_to": "EXTERIOR",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface 1",
                                            "classification": "DOOR",
                                            "glazed_area": 10,
                                            "opaque_area": 2,
                                        },
                                        {
                                            "id": "subsurface 2",
                                            "classification": "WINDOW",
                                            "glazed_area": 10,
                                            "opaque_area": 2,
                                        },
                                    ],
                                },
                                {
                                    "id": "surface 1",
                                    "adjacent_to": "INTERIOR",
                                },
                            ],
                        },
                        {
                            # case has door but the space area is greater than 50 or 2% of the floor area
                            "id": "Thermal Zone 3",
                            "floor_name": "FLOOR 1",
                            "spaces": [
                                {
                                    "id": "Space 4",
                                    "floor_area": 5,
                                },
                            ],
                            "surfaces": [
                                {
                                    "id": "surface 2",
                                    "adjacent_to": "EXTERIOR",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface 3",
                                            "classification": "DOOR",
                                            "glazed_area": 10,
                                            "opaque_area": 2,
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
    "type": "BASELINE_0",
}


TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
}

TEST_RMD_UNIT = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_is_zone_likely_a_vestibule_thermal_zone_1__success():
    assert is_zone_likely_a_vestibule(TEST_RMD_UNIT, "Thermal Zone 1") is False


def test_is_zone_likely_a_vestibule_thermal_zone_2__success():
    assert is_zone_likely_a_vestibule(TEST_RMD_UNIT, "Thermal Zone 2") is False


def test_is_zone_likely_a_vestibule_thermal_zone_3__success():
    assert is_zone_likely_a_vestibule(TEST_RMD_UNIT, "Thermal Zone 3") is True
