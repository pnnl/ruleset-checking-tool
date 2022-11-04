from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_purchased_heating import (
    are_all_terminal_heating_loops_purchased_heating,
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
                                {"id": "terminal_1", "heating_from_loop": "HW_Loop_1"},
                                {"id": "terminal_2", "heating_from_loop": "CHW_Loop_1"},
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
    "external_fluid_source": [
        {"id": "fluid_loop_1", "loop": "HW_Loop_1", "type": "HOT_WATER"},
        {"id": "fluid_loop_2", "loop": "ST_Loop_1", "type": "STEAM"},
        {"id": "fluid_loop_3", "loop": "CHW_Loop_1", "type": "CHILLED_WATER"},
    ],
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__all_terminal_heating_loops_purchased_heating():
    assert (
        are_all_terminal_heating_loops_purchased_heating(TEST_RMD, ["terminal_1"])
        == True
    )


def test__all_terminal_heating_source_not_purchased_heating():
    assert (
        are_all_terminal_heating_loops_purchased_heating(
            TEST_RMD, ["terminal_2", "terminal_3"]
        )
        == False
    )


def test__not_all_terminal_heating_source_purchased_heating():
    assert (
        are_all_terminal_heating_loops_purchased_heating(
            TEST_RMD, ["terminal_1", "terminal_2"]
        )
        == False
    )
