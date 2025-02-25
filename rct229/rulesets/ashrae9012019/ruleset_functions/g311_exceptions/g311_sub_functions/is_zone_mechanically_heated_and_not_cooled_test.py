from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_zone_mechanically_heated_and_not_cooled import (
    is_zone_mechanically_heated_and_not_cooled,
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
                            "heating_system": {
                                "id": "csys_1_1_2",
                                "type": "ELECTRIC_RESISTANCE",
                            },
                        },
                        {
                            "id": "System 2",
                            "cooling_system": {
                                "id": "csys_2_1_1",
                            },
                            "heating_system": {"id": "csys_2_1_2", "type": "NONE"},
                        },
                        {
                            "id": "System 3",
                            "heating_system": {"id": "csys_3_1_2", "type": "NONE"},
                        },
                        {
                            "id": "System 4",
                            "heating_system": {"id": "csys_4_1_2", "type": "FURNACE"},
                        },
                    ],
                    "zones": [
                        # Has cooling system, has heating system - return False
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
                            # Has cooling system, has no heating system - return False
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
                            # Has cooling system (through transfer air), has no heating system - return False
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
                        {
                            # Has no cooling system, heating system from terminal - return True
                            "id": "zone 4",
                            "terminals": [
                                {
                                    "id": "terminal_4_1",
                                    "heating_source": "HOT_WATER",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 3",
                                },
                            ],
                        },
                        {
                            # Has no cooling system, heating system from system - return True
                            "id": "zone 5",
                            "terminals": [
                                {
                                    "id": "terminal_5_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 4",
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
}

TEST_RMD_UNIT = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test_is_zone_mechanically_heated_and_not_cooled_zone_1__false():
    assert is_zone_mechanically_heated_and_not_cooled(TEST_RMD_UNIT, "zone 1") is False


def test_is_zone_mechanically_heated_and_not_cooled_zone_2__false():
    assert is_zone_mechanically_heated_and_not_cooled(TEST_RMD_UNIT, "zone 2") is False


def test_is_zone_mechanically_heated_and_not_cooled_zone_3__false():
    assert is_zone_mechanically_heated_and_not_cooled(TEST_RMD_UNIT, "zone 3") is False


def test_is_zone_mechanically_heated_and_not_cooled_zone_4__true():
    assert is_zone_mechanically_heated_and_not_cooled(TEST_RMD_UNIT, "zone 4") is True


def test_is_zone_mechanically_heated_and_not_cooled_zone_5__true():
    assert is_zone_mechanically_heated_and_not_cooled(TEST_RMD_UNIT, "zone 5") is True
