from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zones_computer_rooms import (
    get_zone_computer_rooms,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMI = {
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
                                    "function": "LABORATORY",
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "floor_area": 100,
                                },
                                {
                                    "id": "Space 2",
                                    "floor_area": 100,
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
}


TEST_RPD_FULL = {"id": "229", "ruleset_model_descriptions": [TEST_RMI]}

TEST_RMD_UNIT = quantify_rmr(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_building_total_lab_exhaust_from_zone_exhaust_fan__success():
    assert get_zone_computer_rooms(TEST_RMD_UNIT) == {
        "Thermal Zone 1": {
            "zone_computer_room_floor_area": 100 * ureg("m2"),
            "total_zone_floor_area": 200 * ureg("m2"),
        }
    }
