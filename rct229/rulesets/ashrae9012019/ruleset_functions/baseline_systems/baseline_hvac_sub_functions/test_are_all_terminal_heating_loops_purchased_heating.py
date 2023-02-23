from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_purchased_heating import (
    are_all_terminal_heating_loops_purchased_heating,
)
from rct229.schema.validate import schema_validate_rmr

TEST_RMI = {
    "id": "test_rmi",
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
                        {
                            "id": "zone 2",
                            "terminals": [
                                {
                                    "id": "terminal_4"
                                },  # intentionally omit `heating_from_loop` key to test out `if are_all_terminal_heating_loops_purchased_heating_flag and heating_from_loop_id:` false case.
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

TEST_RMD = {"id": "229_01", "ruleset_model_instances": [TEST_RMI]}


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__are_all_terminal_heating_loops_purchased_heating__all_terminal_heating_loops_purchased_heating():
    assert (
        are_all_terminal_heating_loops_purchased_heating(TEST_RMI, ["terminal_1"])
        == True
    )


def test__are_all_terminal_heating_loops_purchased_heating__all_terminal_heating_source_not_purchased_heating():
    assert (
        are_all_terminal_heating_loops_purchased_heating(
            TEST_RMI, ["terminal_2", "terminal_3"]
        )
        == False
    )


def test__are_all_terminal_heating_loops_purchased_heating__not_all_terminal_heating_source_purchased_heating():
    assert (
        are_all_terminal_heating_loops_purchased_heating(
            TEST_RMI, ["terminal_1", "terminal_2"]
        )
        == False
    )
