from rct229.rulesets.ashrae9012019.ruleset_functions.compare_swh_dist_systems_and_components import (
    compare_swh_dist_systems_and_components,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rmd
import copy

TEST_RMD = {
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
                                    "service_water_heating_uses": [
                                        {
                                            "id": "SWH Use 1",
                                            "served_by_distribution_system": "SWH Distribution 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Space 2",
                                    "service_water_heating_uses": [
                                        {
                                            "id": "SWH Use 2",
                                            "served_by_distribution_system": "SWH Distribution 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Space 3",
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    ],
    "service_water_heating_distribution_systems": [
        {
            "id": "SWH Distribution 1",
            "tanks": [
                {
                    "id": "Tank 1",
                },
                {
                    "id": "Tank 2",
                },
            ],
            "service_water_piping": [
                {
                    "id": "SWH Piping 1",
                    "child": [
                        {
                            "id": "SWH Piping Child 1",
                            "child": [
                                {
                                    "id": "SWH Piping 1-a",
                                },
                                {
                                    "id": "SWH Piping 1-b",
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": "SWH Piping 2",
                },
            ],
        }
    ],
    "pumps": [
        {
            "id": "Pump 1",
            "loop_or_piping": "SWH Piping 1",
        },
        {
            "id": "Pump 2",
            "loop_or_piping": "SWH Piping 2",
        },
    ],
    "service_water_heating_equipment": [
        {
            "id": "SWH Equipment 1",
            "distribution_system": "SWH Distribution 1",
            "solar_thermal_systems": [
                {
                    "id": "Solar Thermal System 1",
                },
                {
                    "id": "Solar Thermal System 2",
                },
            ],
        },
        {
            "id": "SWH Equipment 2",
            "distribution_system": "SWH Distribution 2",
            "solar_thermal_systems": [
                {
                    "id": "Solar Thermal System 3",
                },
                {
                    "id": "Solar Thermal System 4",
                },
            ],
        },
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD_FIXED_TYPE__is_valid():
    schema_validation_result = schema_validate_rmd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_aggregated_zone_hvac_fan_operating_schedule__correct_mapping():
    assert (
        compare_swh_dist_systems_and_components(
            TEST_RMD, TEST_RMD, "test", "SWH Distribution 1"
        )
        == []
    )
