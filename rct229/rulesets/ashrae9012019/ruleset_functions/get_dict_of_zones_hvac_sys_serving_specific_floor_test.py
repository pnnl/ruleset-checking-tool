from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_hvac_sys_serving_specific_floor import (
    get_dict_of_zones_hvac_sys_serving_specific_floor,
)
from rct229.schema.validate import schema_validate_rmr

TEST_RMI = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "zones": [
                        {
                            "id": "zone 1",
                            "floor_name": "FL 1",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                                {
                                    "id": "terminal_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                            ],
                        },
                        {
                            "id": "zone 2",
                            "floor_name": "FL 2",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                                {
                                    "id": "terminal_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 3",
                                },
                            ],
                        },
                        {
                            "id": "zone 3",
                            "floor_name": "FL 3",
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
    "ruleset_model_descriptions": [TEST_RMI],
    "data_timestamp": "2024-02-12T09:00Z",
}


def test__TEST_RMD_FIXED_TYPE__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_dict_of_zones_hvac_sys_serving_specific_floor__FL1s_system():
    assert get_dict_of_zones_hvac_sys_serving_specific_floor(TEST_RMI, "FL 1") == {
        "zone 1": ["System 1", "System 2"]
    }


def test__get_dict_of_zones_hvac_sys_serving_specific_floor__FL2s_system():
    assert get_dict_of_zones_hvac_sys_serving_specific_floor(TEST_RMI, "FL 2") == {
        "zone 2": ["System 1", "System 3"]
    }


def test__get_dict_of_zones_hvac_sys_serving_specific_floor__zone_not_connected_HVAC():
    assert get_dict_of_zones_hvac_sys_serving_specific_floor(TEST_RMI, "FL 3") == {
        "zone 3": []
    }


def test__get_dict_of_zones_hvac_sys_serving_specific_floor__no_floor():
    assert get_dict_of_zones_hvac_sys_serving_specific_floor(TEST_RMI, "FL 4") == {}
