from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zones_computer_rooms import (
    get_zone_computer_rooms,
)
from rct229.schema.config import ureg
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
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "floor_area": 100,
                                },
                                {
                                    "id": "Space 2",
                                    "floor_area": 100,
                                },
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "spaces": [
                                {
                                    "id": "Space 3",
                                    "floor_area": 10,
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "misc_equipment 1",
                                            "power": 800,
                                            "energy_type": "ELECTRICITY",
                                            "multiplier_schedule": "schedule_1",
                                        },
                                        {
                                            "id": "misc_equipment 2",
                                            "power": 1500,
                                            "energy_type": "ELECTRICITY",
                                            "multiplier_schedule": "schedule_1",
                                        },
                                    ],
                                },
                                {
                                    "id": "Space 4",
                                    "floor_area": 10,
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


def test__get_zones_computer_rooms__success():
    assert get_zone_computer_rooms(TEST_RMD_UNIT) == {
        "Thermal Zone 1": {
            "zone_computer_room_floor_area": 100 * ureg("m2"),
            "total_zone_floor_area": 200 * ureg("m2"),
        },
        "Thermal Zone 2": {
            "zone_computer_room_floor_area": 10 * ureg("m2"),
            "total_zone_floor_area": 20 * ureg("m2"),
        },
    }
