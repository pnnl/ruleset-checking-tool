from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.validate import schema_validate_rmr

TEST_RMI = {
    "id": "test_rmi",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "zones": [
                        {
                            "id": "zone 1",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                                {
                                    "id": "terminal_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                                {
                                    "id": "terminal_3",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                            ],
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


def test__all_terminal_fans_parallel():
    assert get_list_hvac_systems_associated_with_zone(TEST_RMI, "zone 1") == [
        "System 1",
        "System 2",
    ]


def test__all_terminal_fans_parallel__wrong_output():
    assert get_list_hvac_systems_associated_with_zone(TEST_RMI, "zone 1") != [
        "System 1",
        "System 2",
        "System 1",
    ]
