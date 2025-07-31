from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1e import (
    does_zone_meet_g3_1_1e,
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
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 1",
                            "cooling_system": {
                                "id": "csys_1_1_1",
                                "type": "NON_MECHANICAL",
                            },
                            "heating_system": {
                                "id": "csys_1_1_2",
                                "type": "ELECTRIC_RESISTANCE",
                            },
                        },
                        {
                            "id": "System 2",
                            "heating_system": {"id": "csys_2_1_2", "type": "FURNACE"},
                        },
                    ],
                    "zones": [
                        # Not a vestibule, zone has mechanical heating and cooling, space types meet 3_1_1e eligible
                        {
                            "id": "Thermal Zone 1",
                            "floor_name": "FLOOR 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "floor_area": 1000,
                                    "lighting_space_type": "STORAGE_ROOM_HOSPITAL",
                                },
                                {
                                    "id": "Space 2",
                                    "floor_area": 100,
                                    "lighting_space_type": "STORAGE_ROOM_HOSPITAL",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                            ],
                        },
                        # Likely a vestibule, zone has mechanical heating and no cooling,
                        # space type does not meet 3_1_1e eligible
                        {
                            # case has door but the space area is greater than 50 or 2% of the floor area
                            "id": "Thermal Zone 2",
                            "floor_name": "FLOOR 1",
                            "terminals": [
                                {
                                    "id": "terminal_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                            ],
                            "spaces": [
                                {"id": "Space 3", "floor_area": 5},
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


def test__does_zone_meet_g3_1_1e__zone_1_false():
    # false due to zone is mechanically cooled
    assert (
        does_zone_meet_g3_1_1e(TEST_RMD_UNIT, TEST_RMD_UNIT, "Thermal Zone 1") == False
    )


def test__does_zone_meet_g3_1_1e__zone_2_true():
    # true because zone is vestibule and no cooling
    assert (
        does_zone_meet_g3_1_1e(TEST_RMD_UNIT, TEST_RMD_UNIT, "Thermal Zone 2") == True
    )
