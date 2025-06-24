import json
import os
from copy import deepcopy

from rct229.schema.validate import (
    check_unique_ids_in_ruleset_model_descriptions,
    json_paths_to_lists,
    json_paths_to_lists_from_dict,
    json_paths_to_lists_from_list,
    non_schema_validate_rpd,
    validate_rpd,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore, RuleSet


SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
SchemaEnums.update_schema_enum()
EXAMPLES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "examples")

ServiceWaterHeatingUseUnitOptions = SchemaEnums.schema_enums[
    "ServiceWaterHeatingUseUnitOptions"
]
HeatingMetricOptions = SchemaEnums.schema_enums["HeatingMetricOptions"]
CoolingMetricOptions = SchemaEnums.schema_enums["CoolingMetricOptions"]


# Testing validate_rmd; intended to make sure the referenced schemas are connected
# properly and that the example rmd files are schema valid
def test__validate_rmd__with_baseline_rmd():
    with open(os.path.join(EXAMPLES_PATH, "baseline_rmd.json")) as rmd_file:
        rmd_obj = json.load(rmd_file)
    assert validate_rpd(rmd_obj) == {"passed": True, "error": None}


def test__validate_rmd__with_proposed_rmd():
    with open(os.path.join(EXAMPLES_PATH, "proposed_rmd.json")) as rmd_file:
        rmd_obj = json.load(rmd_file)
    assert validate_rpd(rmd_obj) == {"passed": True, "error": None}


def test__validate_rmd__with_user_rmd():
    with open(os.path.join(EXAMPLES_PATH, "user_rmd.json")) as rmd_file:
        rmd_obj = json.load(rmd_file)
    assert validate_rpd(rmd_obj) == {"passed": True, "error": None}


# Testing the three companion functions that find json paths to list

TEST_IDS_RMD = {
    "ruleset_model_descriptions": [
        {
            "id": "rmd_1",
            "buildings": [
                {
                    "id": "bldg_1_1",
                    "building_segments": [
                        {"id": "bs_1_1_1"},
                        {"id": "bs_1_1_2"},
                    ],
                },
                {
                    "id": "bldg_1_2",
                    "building_segments": [
                        {"id": "bs_1_2_1"},
                        # A duplicate
                        {"id": "bs_1_1_2"},
                    ],
                },
            ],
        }
    ]
}

TEST_UNIQUE_IDS_RMD = deepcopy(TEST_IDS_RMD)
TEST_UNIQUE_IDS_RMD["ruleset_model_descriptions"][0]["buildings"][1][
    "building_segments"
][1]["id"] = "bs_1_2_2"


def test__json_paths_to_lists_from_dict():
    assert json_paths_to_lists_from_dict(TEST_IDS_RMD, "$") == {
        "$.ruleset_model_descriptions",
        "$.ruleset_model_descriptions[*].buildings",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments",
    }


def test__json_paths_to_lists_from_list():
    assert json_paths_to_lists_from_list(
        TEST_IDS_RMD["ruleset_model_descriptions"], "$.ruleset_model_descriptions"
    ) == {
        "$.ruleset_model_descriptions",
        "$.ruleset_model_descriptions[*].buildings",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments",
    }


def test__json_paths_to_lists():
    assert json_paths_to_lists(TEST_IDS_RMD) == {
        "$.ruleset_model_descriptions",
        "$.ruleset_model_descriptions[*].buildings",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments",
    }


# -----------------------------------------------


def test__check_unique_ids_in_ruleset_model_descriptions__not_unique():
    assert (
        check_unique_ids_in_ruleset_model_descriptions(TEST_IDS_RMD)
        == "Non-unique ids for paths: ruleset_model_descriptions[0].buildings[*].building_segments"
    )


def test__check_unique_ids_in_ruleset_model_descriptions__unique():
    assert check_unique_ids_in_ruleset_model_descriptions(TEST_UNIQUE_IDS_RMD) == ""


# -----------------------------------------------


def test__non_schema_validate_rpd__not_unique():
    assert non_schema_validate_rpd(TEST_IDS_RMD) == {
        "passed": False,
        "error": [
            "Non-unique ids for paths: ruleset_model_descriptions[0].buildings[*].building_segments",
        ],
    }


def test__non_schema_validate_rpd__unique():
    assert non_schema_validate_rpd(TEST_UNIQUE_IDS_RMD) == {
        "passed": True,
        "error": None,
    }


TEST_MISMATCHED_LISTS_RMD = {
    "ruleset_model_descriptions": [
        {
            "id": "RMD 1",
            "buildings": [
                {
                    "id": "Bldg 1",
                    "building_segments": [
                        {
                            "id": "Segment 1",
                            "zones": [
                                {
                                    "id": "Zone 1",
                                    "spaces": [
                                        {
                                            "id": "Space 1",
                                            "service_water_heating_uses": [
                                                "SWH Use 1",
                                            ],
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "HVAC 1",
                                    "preheat_system": {"id": "Preheat 1"},
                                    "heating_system": {"id": "Heating 1"},
                                    "cooling_system": {"id": "Cooling 1"},
                                }
                            ],
                            "service_water_heating_uses": [
                                "Typical SWH Use",
                            ],
                        },
                    ],
                }
            ],
            "boilers": [{"id": "Boiler 1"}],
            "chillers": [{"id": "Chiller 1"}],
            "service_water_heating_uses": [
                {"id": "Typical SWH Use"},
                {"id": "SWH Use 1"},
            ],
            "service_water_heating_equipment": [{"id": "SWH Equipment 1"}],
            "service_water_heating_uses": [
                {"id": "SWH Use 1"},
                {"id": "Typical SWH Use"},
            ],
        }
    ]
}


def test__non_schema_validate_rpd__missing_associated_swh_use_lists_1():
    test_rmd = deepcopy(TEST_MISMATCHED_LISTS_RMD)
    test_rmd["ruleset_model_descriptions"][0]["service_water_heating_uses"][1][
        "use"
    ] = [3]
    assert non_schema_validate_rpd(test_rmd) == {
        "passed": False,
        "error": ["'Typical SWH Use' has populated 'use' but is missing 'use_units'."],
    }


def test__non_schema_validate_rpd__mismatched_associated_swh_use_lists_1():
    test_rmd = deepcopy(TEST_MISMATCHED_LISTS_RMD)
    test_rmd["ruleset_model_descriptions"][0]["service_water_heating_uses"][1][
        "use"
    ] = [3, 4, 5]
    test_rmd["ruleset_model_descriptions"][0]["service_water_heating_uses"][1][
        "use_units"
    ] = [
        ServiceWaterHeatingUseUnitOptions.POWER,
        ServiceWaterHeatingUseUnitOptions.VOLUME,
    ]

    assert non_schema_validate_rpd(test_rmd) == {
        "passed": False,
        "error": [
            "'Typical SWH Use' lists at 'use_units' and 'use' are not the same length."
        ],
    }


def test__non_schema_validate_rpd__mismatched_associated_swh_use_lists_2():
    test_rmd = deepcopy(TEST_MISMATCHED_LISTS_RMD)
    test_rmd["ruleset_model_descriptions"][0]["service_water_heating_uses"][0][
        "use"
    ] = [3, 4, 5]
    test_rmd["ruleset_model_descriptions"][0]["service_water_heating_uses"][0][
        "use_units"
    ] = [
        ServiceWaterHeatingUseUnitOptions.POWER,
        ServiceWaterHeatingUseUnitOptions.VOLUME,
    ]

    assert non_schema_validate_rpd(test_rmd) == {
        "passed": False,
        "error": [
            "'SWH Use 1' lists at 'use_units' and 'use' are not the same length."
        ],
    }


def test__non_schema_validate_rpd__mismatched_associated_efficiency_lists_1():
    test_rmd = deepcopy(TEST_MISMATCHED_LISTS_RMD)
    test_rmd["ruleset_model_descriptions"][0]["buildings"][0]["building_segments"][0][
        "heating_ventilating_air_conditioning_systems"
    ][0]["preheat_system"]["efficiency_metric_types"] = [
        HeatingMetricOptions.THERMAL_EFFICIENCY
    ]
    test_rmd["ruleset_model_descriptions"][0]["buildings"][0]["building_segments"][0][
        "heating_ventilating_air_conditioning_systems"
    ][0]["preheat_system"]["efficiency_metric_values"] = [
        0.8,
        3.4,
    ]

    assert non_schema_validate_rpd(test_rmd) == {
        "passed": False,
        "error": [
            "'Preheat 1' lists at 'efficiency_metric_types' and 'efficiency_metric_values' are not the same length."
        ],
    }


def test__non_schema_validate_rpd__mismatched_associated_efficiency_lists_2():
    test_rmd = deepcopy(TEST_MISMATCHED_LISTS_RMD)
    test_rmd["ruleset_model_descriptions"][0]["buildings"][0]["building_segments"][0][
        "heating_ventilating_air_conditioning_systems"
    ][0]["cooling_system"]["efficiency_metric_types"] = [
        CoolingMetricOptions.FULL_LOAD_COEFFICIENT_OF_PERFORMANCE
    ]
    test_rmd["ruleset_model_descriptions"][0]["buildings"][0]["building_segments"][0][
        "heating_ventilating_air_conditioning_systems"
    ][0]["cooling_system"]["efficiency_metric_values"] = [
        3.4,
        3.2,
    ]

    assert non_schema_validate_rpd(test_rmd) == {
        "passed": False,
        "error": [
            "'Cooling 1' lists at 'efficiency_metric_types' and 'efficiency_metric_values' are not the same length."
        ],
    }
