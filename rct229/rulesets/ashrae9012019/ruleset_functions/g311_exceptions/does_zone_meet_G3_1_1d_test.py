from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1d import (
    does_zone_meet_g3_1_1d,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "hvac 1",
                            "fan_system": {
                                "id": "fan_system_1",
                                "exhaust_fans": [
                                    {
                                        "id": "exhaust_fans 1",
                                        "design_airflow": 7500,
                                    }
                                ],
                            },
                        }
                    ],
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "function": "LABORATORY",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "Terminal 1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac 1",
                                    "primary_airflow": 6500,
                                }
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Exhaust Fan 1",
                                    "design_airflow": 1000,
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "terminals": [
                                {
                                    "id": "Terminal 2",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac 1",
                                    "primary_airflow": 1000,
                                }
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
    "ruleset_model_descriptions": [TEST_RMD],
}

TEST_RMD_UNIT = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__does_zone_meet_g3_1_1_d__hvac_100_percent_terminals__success():
    assert does_zone_meet_g3_1_1d(TEST_RMD_UNIT, "Thermal Zone 1") == True


def test__does_zone_meet_g3_1_1_d__not_lab__failed():
    assert does_zone_meet_g3_1_1d(TEST_RMD_UNIT, "Thermal Zone 2") == False
