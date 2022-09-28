from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_electric import (
    are_all_terminal_heat_sources_electric,
)

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "zones": [
                        {
                            "id": "zone 1",
                            "terminals": [
                                {"id": "terminal_1"},
                                {"id": "terminal_2", "heating_source": "HOT_WATER"},
                                {"id": "terminal_3", "heating_source": "ELECTRIC"},
                            ],
                        },
                    ],
                }
            ],
        }
    ],
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__all_terminal_heat_source_hot_water():
    assert are_all_terminal_heat_sources_electric(TEST_RMD, ["terminal_2"]) == False


def test__all_terminal_heat_source_electric():
    assert are_all_terminal_heat_sources_electric(TEST_RMD, ["terminal_3"]) == True


def test__all_terminal_heat_source_none():
    assert are_all_terminal_heat_sources_electric(TEST_RMD, ["terminal_1"]) == False
