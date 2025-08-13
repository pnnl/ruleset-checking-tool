from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_computer_zones_peak_cooling_load import (
    get_computer_zones_peak_cooling_load,
)
from rct229.schema.config import ureg
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
                                            "power": 500,
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
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RMD_UNIT = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_computer_zones_peak_cooling_load__success():
    assert get_computer_zones_peak_cooling_load(TEST_RMD_UNIT) == 1500 * ureg(
        "watt"
    ).to("Btu/hr")
