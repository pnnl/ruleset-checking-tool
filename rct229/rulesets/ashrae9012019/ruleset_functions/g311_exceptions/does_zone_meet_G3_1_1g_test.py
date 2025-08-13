from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1g import (
    does_zone_meet_g3_1_1g,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "floor_area": 500,
                                    "interior_lighting": [
                                        {
                                            "id": "interior_lighting_1",
                                            "lighting_multiplier_schedule": "lighting_schedule_1",
                                            "power_per_area": 1.0,
                                        }
                                    ],
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "miscellaneous_equipment_1",
                                            "multiplier_schedule": "miscellaneous_equipment_schedule_1",
                                            "power": 500000,
                                        }
                                    ],
                                    "occupant_multiplier_schedule": "occupant_schedule_1",
                                    "occupant_sensible_heat_gain": 125,
                                    "occupant_latent_heat_gain": 125,
                                },
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "spaces": [
                                {
                                    "id": "Space 2",
                                    "floor_area": 500,
                                    "interior_lighting": [
                                        {
                                            "id": "interior_lighting_2",
                                            "lighting_multiplier_schedule": "lighting_schedule_1",
                                            "power_per_area": 1.0,
                                        }
                                    ],
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "miscellaneous_equipment_2",
                                            "multiplier_schedule": "miscellaneous_equipment_schedule_1",
                                            "power": 100,
                                        }
                                    ],
                                    "occupant_multiplier_schedule": "occupant_schedule_1",
                                    "occupant_sensible_heat_gain": 125,
                                    "occupant_latent_heat_gain": 125,
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
    "schedules": [
        {"id": "schedule_1", "hourly_values": [1.2] * 8670},
        {"id": "lighting_schedule_1", "hourly_cooling_design_day": [1] * 24},
        {
            "id": "miscellaneous_equipment_schedule_1",
            "hourly_cooling_design_day": [1] * 24,
        },
        {"id": "occupant_schedule_1", "hourly_cooling_design_day": [1] * 23 + [2] * 1},
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


def test__does_zone_meet_g3_1_1g__thermal_zone_1_true():
    assert does_zone_meet_g3_1_1g(TEST_RMD_UNIT, "Thermal Zone 1") == True


def test__does_zone_meet_g3_1_1g__thermal_zone_2_false():
    assert does_zone_meet_g3_1_1g(TEST_RMD_UNIT, "Thermal Zone 2") == False
