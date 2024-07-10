from rct229.rulesets.ashrae9012019.ruleset_functions.get_HVAC_systems_primarily_serving_comp_rooms import (
    get_HVAC_systems_primarily_serving_comp_rooms,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rmd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                {
                    "id": "bldg_seg_1",
                    "zones": [
                        {
                            "id": "zone_1",
                            "spaces": [
                                # The overall area ratio of the computer room < 0.5
                                {
                                    "id": "space_1_1",
                                    "floor_area": 1000,
                                    "lighting_space_type": "COMPUTER_ROOM",
                                },
                                {
                                    "id": "space_1_2",
                                    "floor_area": 500,
                                    "lighting_space_type": "ATRIUM_HIGH",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_1_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1",
                                }
                            ],
                        },
                        {
                            "id": "zone_2",
                            "spaces": [
                                # The overall area ratio of the computer room > 0.5
                                {
                                    "id": "space_2_1",
                                    "floor_area": 1500,
                                    "lighting_space_type": "COMPUTER_ROOM",
                                },
                                {
                                    "id": "space_2_2",
                                    "floor_area": 250,
                                    "lighting_space_type": "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2",
                                }
                            ],
                        },
                        {
                            "id": "zone_3",
                            "spaces": [
                                # The overall area ratio of the computer room < 0.5
                                {
                                    "id": "space_3_1",
                                    "floor_area": 250,
                                    "lighting_space_type": "COMPUTER_ROOM",
                                },
                                {
                                    "id": "space_3_2",
                                    "floor_area": 800,
                                    "lighting_space_type": "DINING_AREA_BAR_LOUNGE_OR_LEISURE_DINING",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_3_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_3",
                                }
                            ],
                        },
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "hvac_1",
                        },
                        {
                            "id": "hvac_2",
                        },
                        {
                            "id": "hvac_3",
                        },
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}
TEST_RMD = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD_UNIT = quantify_rmd(TEST_RMD)["ruleset_model_descriptions"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmd(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_HVAC_systems_primarily_serving_comp_rooms__success():
    assert get_HVAC_systems_primarily_serving_comp_rooms(TEST_RMD_UNIT) == [
        "hvac_1",
        "hvac_2",
    ]
