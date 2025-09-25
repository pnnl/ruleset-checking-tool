import copy

from rct229.rulesets.ashrae9012019.ruleset_functions.compare_swh_dist_systems_and_components import (
    compare_swh_dist_systems_and_components,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "served_by_distribution_system": "SWH Distribution 1",
        },
        {
            "id": "SWH Use 2",
            "served_by_distribution_system": "SWH Distribution 1",
        },
    ],
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
                                    "service_water_heating_uses": ["SWH Use 1"],
                                },
                                {
                                    "id": "Space 2",
                                    "service_water_heating_uses": ["SWH Use 2"],
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    ],
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "served_by_distribution_system": "SWH Distribution 1",
        },
        {
            "id": "SWH Use 2",
            "served_by_distribution_system": "SWH Distribution 1",
        },
    ],
    "service_water_heating_distribution_systems": [
        {
            "id": "SWH Distribution 1",
            "tanks": [
                {
                    "id": "Tank 1",
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
        },
        {
            "id": "SWH Distribution 2",
            "tanks": [
                {
                    "id": "Tank 2",
                },
            ],
            "service_water_piping": {
                "id": "SWH Piping 2",
                "child": [
                    {
                        "id": "SWH Piping Child 2",
                        "child": [
                            {
                                "id": "SWH Piping 2-a",
                            }
                        ],
                    }
                ],
            },
        },
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
}

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


TEST_RMD_COPIED = copy.deepcopy(TEST_RMD)

# Change the values
TEST_RMD_COPIED["service_water_heating_distribution_systems"][1][
    "service_water_piping"
]["id"] = "SWH Piping a"
TEST_RMD_COPIED["pumps"][1]["loop_or_piping"] = "SWH Piping a"
TEST_RMD_COPIED["service_water_heating_distribution_systems"][1][
    "service_water_piping"
]["child"][0]["id"] = "SWH Piping Child a"
TEST_RMD_COPIED["service_water_heating_equipment"][1]["solar_thermal_systems"][0][
    "id"
] = "Solar Thermal System a"

TEST_RPD_COPIED_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_COPIED],
}

TEST_RMD_COPIED = quantify_rmd(TEST_RPD_COPIED_FULL)["ruleset_model_descriptions"][0]

# Make a copy of another RMD to test the different swh_equipment length
TEST_RMD_COPIED_DIFF_SWH_EQUIP_LEN = copy.deepcopy(TEST_RMD)

TEST_RMD_COPIED_DIFF_SWH_EQUIP_LEN["service_water_heating_equipment"].append(
    {
        "id": "SWH Equipment 3",
        "distribution_system": "SWH Distribution 2",
        "solar_thermal_systems": [
            {
                "id": "Solar Thermal System 3",
            },
            {
                "id": "Solar Thermal System 4",
            },
        ],
    }
)

TEST_RMD_NO_MATCH = copy.deepcopy(TEST_RMD)
TEST_RMD_NO_MATCH["pumps"][1]["loop_or_piping"] = "SWH Piping a"


TEST_RPD_COPIED_DIFF_SWH_EQUIP_LEN_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_COPIED_DIFF_SWH_EQUIP_LEN],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RMD_COPIED_DIFF_SWH_EQUIP_LEN_FULL = quantify_rmd(
    TEST_RPD_COPIED_DIFF_SWH_EQUIP_LEN_FULL
)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RPD_Copied__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_COPIED_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RPD_Copied_diff_len__is_valid():
    schema_validation_result = schema_validate_rpd(
        TEST_RPD_COPIED_DIFF_SWH_EQUIP_LEN_FULL
    )
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__compare_swh_dist_systems_and_components__all_match():
    assert (
        compare_swh_dist_systems_and_components(
            TEST_RMD, TEST_RMD, "AppG Used By TCDs", "SWH Distribution 1"
        )
        == []
    )


def test__compare_swh_dist_systems_and_components__pump_not_matched():
    assert compare_swh_dist_systems_and_components(
        TEST_RMD, TEST_RMD_COPIED, "AppG Used By TCDs", "SWH Distribution 2"
    ) == [
        "path: $.service_water_heating_distribution_systems[SWH Distribution 2].service_water_piping: data object SWH Piping 2 in index context does not match the one SWH Piping a in compare context",
        "path: $.service_water_heating_distribution_systems[SWH Distribution 2].service_water_piping.child[0]: data object SWH Piping Child 2 in index context does not match the one SWH Piping Child a in compare context",
        "path: $.service_water_heating_equipment[SWH Equipment 2].solar_thermal_systems[0]: data object Solar Thermal System 3 in index context does not match the one Solar Thermal System 4 in compare context",
        "path: $.service_water_heating_equipment[SWH Equipment 2].solar_thermal_systems[1]: data object Solar Thermal System 4 in index context does not match the one Solar Thermal System a in compare context",
        "path: $.pumps[Pump 2].loop_or_piping: index context data: SWH Piping 2 does not equal to compare context data: SWH Piping a",
    ]  # The change was because we added index to match the id - if id failed matching, the object will be reported in the mismatch report.


def test__compare_swh_dist_systems_and_components__diff_swh_equipment_length():
    assert compare_swh_dist_systems_and_components(
        TEST_RMD,
        TEST_RMD_COPIED_DIFF_SWH_EQUIP_LEN,
        "AppG Used By TCDs",
        "SWH Distribution 2",
    ) == [
        "Unequal numbers of SWH Equipment between the two models for SWH Distribution 2"
    ]
