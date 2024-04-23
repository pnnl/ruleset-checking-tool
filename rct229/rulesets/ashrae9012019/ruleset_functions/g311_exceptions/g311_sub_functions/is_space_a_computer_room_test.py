from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_space_a_computer_room import (
    is_space_a_computer_room,
)
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMI = {
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
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "function": "LABORATORY",
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "floor_area": 100,
                                },
                                {
                                    "id": "Space 2",
                                    "floor_area": 10,
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "misc_equipment 1",
                                            "energy_type": "ELECTRICITY",
                                            "power": 1000,
                                        },
                                        {
                                            "id": "misc_equipment 2",
                                            "energy_type": "ELECTRICITY",
                                            "power": 2000,
                                        },
                                    ],
                                },
                                {
                                    # max multiplier is 0.7 - does not meet requirements (19W/ft2)
                                    "id": "Space 3",
                                    "floor_area": 10,
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "misc_equipment 1",
                                            "power": 600,
                                            "energy_type": "ELECTRICITY",
                                            "multiplier_schedule": "schedule_1",
                                        },
                                        {
                                            "id": "misc_equipment 2",
                                            "power": 1000,
                                            "energy_type": "ELECTRICITY",
                                            "multiplier_schedule": "schedule_1",
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
    "ruleset_model_descriptions": [TEST_RMI],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD_UNIT = quantify_rmr(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_space_a_compuetr_room_space_type_computer_room__success():
    assert is_space_a_computer_room(TEST_RMD_UNIT, "Space 1") == True


def test__is_space_a_compuetr_room_no_schedule_power_over_threshold__success():
    assert is_space_a_computer_room(TEST_RMD_UNIT, "Space 2") == True


def test__is_space_a_compuetr_room_has_schedules_power_below_threshold__failed():
    assert is_space_a_computer_room(TEST_RMD_UNIT, "Space 3") == False
