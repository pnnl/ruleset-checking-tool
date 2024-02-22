from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_heating import (
    get_proposed_hvac_modeled_with_virtual_heating,
)
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMD_P_HEATING_SYSTEM = {
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
                                    "heating_system": {
                                        "id": "heating_system 1",
                                        "type": "HEAT_PUMP",
                                    },
                                },
                                {
                                    "id": "hvac_2",
                                    "heating_system": {
                                        "id": "heating_system 2",
                                        "type": "HEAT_PUMP",
                                    },
                                },
                                {
                                    "id": "hvac_3",
                                    "heating_system": {
                                        "id": "heating_system 3",
                                        "type": "HEAT_PUMP",
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "type": "PROPOSED",
        }
    ],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD_U_HEATING_SYSTEM = {
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
                                    "heating_system": {
                                        "id": "heating_system 1",
                                    },
                                },
                                {
                                    "id": "hvac_2",
                                    "heating_system": {
                                        "id": "heating_system 2",
                                        "type": "NONE",
                                    },
                                },
                                {
                                    "id": "hvac_3",
                                    "heating_system": {
                                        "id": "heating_system 3",
                                        "type": "HEAT_PUMP",
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "type": "USER",
        }
    ],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD_P_PREHEAT_SYSTEM = {
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
                                    "preheat_system": {
                                        "id": "preheat_system 1",
                                        "type": "HEAT_PUMP",
                                    },
                                },
                                {
                                    "id": "hvac_2",
                                    "preheat_system": {
                                        "id": "preheat_system 2",
                                        "type": "HEAT_PUMP",
                                    },
                                },
                                {
                                    "id": "hvac_3",
                                    "preheat_system": {
                                        "id": "preheat_system 3",
                                        "type": "HEAT_PUMP",
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "type": "PROPOSED",
        }
    ],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD_U_PREHEAT_SYSTEM = {
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
                                    "preheat_system": {
                                        "id": "preheat_system 1",
                                    },
                                },
                                {
                                    "id": "hvac_2",
                                    "preheat_system": {
                                        "id": "preheat_system 2",
                                        "type": "NONE",
                                    },
                                },
                                {
                                    "id": "hvac_3",
                                    "preheat_system": {
                                        "id": "preheat_system 3",
                                        "type": "HEAT_PUMP",
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "type": "USER",
        }
    ],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMI_P_HEATING_SYSTEM = quantify_rmr(TEST_RMD_P_HEATING_SYSTEM)[
    "ruleset_model_descriptions"
][0]
TEST_RMI_U_HEATING_SYSTEM = quantify_rmr(TEST_RMD_U_HEATING_SYSTEM)[
    "ruleset_model_descriptions"
][0]
TEST_RMI_P_PREHEAT_SYSTEM = quantify_rmr(TEST_RMD_P_PREHEAT_SYSTEM)[
    "ruleset_model_descriptions"
][0]
TEST_RMI_U_PREHEAT_SYSTEM = quantify_rmr(TEST_RMD_U_PREHEAT_SYSTEM)[
    "ruleset_model_descriptions"
][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_P_HEATING_SYSTEM)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"
    schema_validation_result = schema_validate_rmr(TEST_RMD_U_HEATING_SYSTEM)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"
    schema_validation_result = schema_validate_rmr(TEST_RMD_P_PREHEAT_SYSTEM)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"
    schema_validation_result = schema_validate_rmr(TEST_RMD_U_PREHEAT_SYSTEM)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_proposed_hvac_modeled_with_virtual_heating__heating_system_success():
    assert get_proposed_hvac_modeled_with_virtual_heating(
        TEST_RMI_U_HEATING_SYSTEM, TEST_RMI_P_HEATING_SYSTEM
    ) == ["hvac_1", "hvac_2"]


def test__get_proposed_hvac_modeled_with_virtual_heating__preheat_system_success():
    assert get_proposed_hvac_modeled_with_virtual_heating(
        TEST_RMI_U_PREHEAT_SYSTEM, TEST_RMI_P_PREHEAT_SYSTEM
    ) == ["hvac_1", "hvac_2"]
