from rct229.rulesets.ashrae9012019.ruleset_functions.are_all_terminal_types_VAV import (
    are_all_terminal_types_VAV,
)
from rct229.schema.validate import schema_validate_rmd


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
                            "id": "zone_1",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "type": "VARIABLE_AIR_VOLUME",
                                },
                                {
                                    "id": "terminal_2",
                                    "type": "CONSTANT_AIR_VOLUME",
                                },
                                {"id": "terminal_3"},
                            ],
                        },
                        {
                            "id": "zone_2",
                            "terminals": [
                                {
                                    "id": "terminal_6",
                                    "type": "VARIABLE_AIR_VOLUME",
                                }
                            ],
                        },
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "hvac_1",
                        }
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}


TEST_RMD = {
    "id": "ASHRAE229",
    "ruleset_model_descriptions": [TEST_RMI],
    "data_timestamp": "2024-02-12T09:00Z",
}


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmd(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__hvac_fan_all_VAV__success():
    assert are_all_terminal_types_VAV(TEST_RMI, ["terminal_1"]) is True


def test__hvac_fan_not_all_VAV__success():
    assert are_all_terminal_types_VAV(TEST_RMI, ["terminal_1", "terminal_2"]) is False


def test__hvac_fan_include_no_type__success():
    assert are_all_terminal_types_VAV(TEST_RMI, ["terminal_1", "terminal_3"]) is True
