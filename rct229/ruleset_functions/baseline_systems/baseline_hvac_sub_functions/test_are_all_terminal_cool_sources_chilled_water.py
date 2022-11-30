from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_chilled_water import (
    are_all_terminal_cool_sources_chilled_water,
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
                                {"id": "terminal_1", "cooling_source": "NONE"},
                                {"id": "terminal_2", "cooling_source": "CHILLED_WATER"},
                                {"id": "terminal_3"},
                            ],
                        },
                    ],
                }
            ],
        }
    ],
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__all_terminal_heat_source_chilled_water_none():
    assert (
        are_all_terminal_cool_sources_chilled_water(
            TEST_RMD, ["terminal_1", "terminal_3"]
        )
        == False
    )


def test__all_terminal_heat_source_chilled_water():
    assert are_all_terminal_cool_sources_chilled_water(TEST_RMD, ["terminal_2"]) == True
