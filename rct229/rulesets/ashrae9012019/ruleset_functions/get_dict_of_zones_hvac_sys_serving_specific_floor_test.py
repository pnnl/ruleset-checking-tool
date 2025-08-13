from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_hvac_sys_serving_specific_floor import (
    get_dict_of_zones_hvac_sys_serving_specific_floor,
)
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
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

TEST_RPD = {
    "id": "229_01",
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


def test__TEST_RPD_FIXED_TYPE__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_dict_of_zones_hvac_sys_serving_specific_floor__FL1s_system():
    assert get_dict_of_zones_hvac_sys_serving_specific_floor(TEST_RMD, "FL 1") == {
        "zone 1": ["System 1", "System 2"]
    }


def test__get_dict_of_zones_hvac_sys_serving_specific_floor__FL2s_system():
    assert get_dict_of_zones_hvac_sys_serving_specific_floor(TEST_RMD, "FL 2") == {
        "zone 2": ["System 1", "System 3"]
    }


def test__get_dict_of_zones_hvac_sys_serving_specific_floor__zone_not_connected_HVAC():
    assert get_dict_of_zones_hvac_sys_serving_specific_floor(TEST_RMD, "FL 3") == {
        "zone 3": []
    }


def test__get_dict_of_zones_hvac_sys_serving_specific_floor__no_floor():
    assert get_dict_of_zones_hvac_sys_serving_specific_floor(TEST_RMD, "FL 4") == {}
