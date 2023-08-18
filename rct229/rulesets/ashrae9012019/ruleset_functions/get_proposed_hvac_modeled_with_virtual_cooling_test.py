from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_cooling import (
    get_proposed_hvac_modeled_with_virtual_cooling,
)
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMD_P_COOLING_SYSTEM = {
    "id": "ashrae229",
    "ruleset_model_descriptions": [
        {
            "id": "test_rmi",
            "buildings": [
                {
                    "id": "building_1",
                    "building_segments": [
                        {
                            "id": "building_segment_1",
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "hvac_1",
                                    "cooling_system": {
                                        "id": "cooling_system 1",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                },
                                {
                                    "id": "hvac_2",
                                    "cooling_system": {
                                        "id": "cooling_system 2",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                },
                                {
                                    "id": "hvac_3",
                                    "cooling_system": {
                                        "id": "cooling_system 3",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    ],
}

TEST_RMD_U_COOLING_SYSTEM = {
    "id": "ashrae229",
    "ruleset_model_descriptions": [
        {
            "id": "test_rmi",
            "buildings": [
                {
                    "id": "building_1",
                    "building_segments": [
                        {
                            "id": "building_segment_1",
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "hvac_1",
                                    "cooling_system": {
                                        "id": "cooling_system 1",
                                    },
                                },
                                {
                                    "id": "hvac_2",
                                    "cooling_system": {
                                        "id": "cooling_system 2",
                                        "type": "NONE",
                                    },
                                },
                                {
                                    "id": "hvac_3",
                                    "cooling_system": {
                                        "id": "cooling_system 3",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    ],
}

TEST_RMI_P_COOLING_SYSTEM = quantify_rmr(TEST_RMD_P_COOLING_SYSTEM)[
    "ruleset_model_descriptions"
][0]
TEST_RMI_U_COOLING_SYSTEM = quantify_rmr(TEST_RMD_U_COOLING_SYSTEM)[
    "ruleset_model_descriptions"
][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_P_COOLING_SYSTEM)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"
    schema_validation_result = schema_validate_rmr(TEST_RMD_U_COOLING_SYSTEM)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_proposed_hvac_modeled_with_virtual_cooling__cooling_system_success():
    assert get_proposed_hvac_modeled_with_virtual_cooling(
        TEST_RMI_U_COOLING_SYSTEM, TEST_RMI_P_COOLING_SYSTEM
    ) == ["hvac_1", "hvac_2"]
