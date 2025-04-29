from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_zone_mechanically_cooled import (
    is_zone_mechanically_cooled,
)
from rct229.schema.schema_utils import quantify_rmd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 1",
                            "cooling_system": {
                                "id": "csys_1_1_1",
                                "type": "NON_MECHANICAL",
                            },
                        },
                        {
                            "id": "System 2",
                            "cooling_system": {
                                "id": "csys_2_1_1",
                            },
                        },
                    ],
                    "zones": [
                        {
                            "id": "zone 1",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                            ],
                        },
                        {
                            "id": "zone 2",
                            "terminals": [
                                {
                                    "id": "terminal_2_1",
                                    "cooling_source": "NONE",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                                {
                                    "id": "terminal_2_2",
                                    "cooling_source": "CHILLED_WATER",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                            ],
                        },
                        {
                            "id": "zone 3",
                            "transfer_airflow_rate": 1000,
                            "transfer_airflow_source_zone": "zone 2",
                            "terminals": [
                                {
                                    "id": "terminal_3_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                                {
                                    "id": "terminal_3_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
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

TEST_RMD_UNIT = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test_is_zone_mechanically_cooled_zone_1__success():
    assert is_zone_mechanically_cooled(TEST_RMD_UNIT, "zone 1") == True


def test_is_zone_mechanically_cooled_zone_2__success():
    assert is_zone_mechanically_cooled(TEST_RMD_UNIT, "zone 2") == True


def test_is_zone_mechanically_cooled_zone_3__success():
    assert is_zone_mechanically_cooled(TEST_RMD_UNIT, "zone 3") == True
