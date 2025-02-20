from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_chw_loops_purcahsed_cooling import (
    are_all_terminal_chw_loops_purchased_cooling,
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
                                {"id": "terminal_1", "cooling_from_loop": "CHW_Loop_1"},
                                {"id": "terminal_2", "cooling_from_loop": "HW_Loop_1"},
                                {"id": "terminal_3"},
                            ],
                        },
                    ],
                }
            ],
        }
    ],
    "fluid_loops": [
        {"id": "HW_Loop_1", "type": "HEATING"},
        {"id": "CHW_Loop_1", "type": "COOLING"},
    ],
    "external_fluid_sources": [
        {"id": "fluid_loop_1", "loop": "HW_Loop_1", "type": "HOT_WATER"},
        {"id": "fluid_loop_2", "loop": "ST_Loop_1", "type": "STEAM"},
        {"id": "fluid_loop_3", "loop": "CHW_Loop_1", "type": "CHILLED_WATER"},
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229_01",
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


def test__all_terminal_cooling_loops_purchased_cooling_all_are_cooling():
    assert (
        are_all_terminal_chw_loops_purchased_cooling(TEST_RMD, ["terminal_1"]) == True
    )


def test__all_terminal_cooling_loops_purchased_cooling_not_all_are():
    assert (
        are_all_terminal_chw_loops_purchased_cooling(
            TEST_RMD, ["terminal_1", "terminal_2"]
        )
        == False
    )


def test__all_terminal_cooling_loops_purchased_cooling_null():
    assert (
        are_all_terminal_chw_loops_purchased_cooling(TEST_RMD, ["terminal_3"]) == False
    )
