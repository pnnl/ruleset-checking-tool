from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_components_associated_with_each_swh_bat import (
    get_swh_components_associated_with_each_swh_bat,
)

from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd
from rct229.schema.config import ureg
from rct229.utils.std_comparisons import std_equal

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
                                    "service_water_heating_area_type": "LIBRARY",
                                    "service_water_heating_uses": ["SWH Use 1"],
                                },
                                {
                                    "id": "Space 2",
                                    "service_water_heating_area_type": "CONVENIENCE_STORE",
                                    "service_water_heating_uses": ["SWH Use 2"],
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
    "schedules": [
        {
            "id": "SWH Schedule 1",
            "hourly_values": [0.8] * 8760,
        },
        {
            "id": "SWH Entering Water Temp Schedule 1",
            "hourly_values": [50] * 8760,
        },
    ],
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "use": 400,
            "use_units": "POWER",
            "is_heat_recovered_by_drain": False,
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "SWH Use 2",
            "use": 100,
            "use_units": "POWER",
            "is_heat_recovered_by_drain": False,
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
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
            "service_water_piping": {
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
        }
    ],
    "pumps": [
        {
            "id": "Pump 1",
            "loop_or_piping": "SWH Piping 1",
        },
        {
            "id": "Pump 3",
            "loop_or_piping": "HVAC Piping 1",
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
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_swh_components_associated_with_each_swh_bat():
    actual_result = get_swh_components_associated_with_each_swh_bat(TEST_RMD)
    assert (
        len(actual_result) == 1
        and std_equal(
            actual_result["LIBRARY"].energy_required, 11956142.6 * ureg("Btu")
        )
        and actual_result["LIBRARY"].swh_distribution == ["SWH Distribution 1"]
        and actual_result["LIBRARY"].swh_heating_eq == ["SWH Equipment 1"]
        and actual_result["LIBRARY"].pumps == ["Pump 1"]
        and actual_result["LIBRARY"].tanks == ["Tank 1", "Tank 2"]
        and actual_result["LIBRARY"].piping
        == [
            "SWH Piping 1",
            "SWH Piping Child 1",
            "SWH Piping 1-a",
            "SWH Piping 1-b",
        ]
        and actual_result["LIBRARY"].solar_thermal
        == ["Solar Thermal System 1", "Solar Thermal System 2"]
        and actual_result["LIBRARY"].swh_uses == ["SWH Use 1", "SWH Use 2"]
    )
