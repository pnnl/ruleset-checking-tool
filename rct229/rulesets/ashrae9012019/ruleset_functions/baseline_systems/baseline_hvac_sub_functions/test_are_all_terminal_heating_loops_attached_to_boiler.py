from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_attached_to_boiler import (
    are_all_terminal_heating_loops_attached_to_boiler,
)
from rct229.schema.validate import schema_validate_rmr

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
                                {"id": "terminal_2", "heating_from_loop": "HW_Loop_2"},
                                {"id": "terminal_3"},
                            ],
                        },
                    ],
                }
            ],
        }
    ],
    "boilers": [{"id": "boiler_1", "loop": "HW_Loop_1"}],
    "fluid_loops": [
        {"id": "HW_Loop_1", "type": "HEATING"},
        {"id": "HW_Loop_2", "type": "HEATING"},
        {"id": "CHW_Loop_1", "type": "COOLING"},
    ],
    "external_fluid_source": [
        {"id": "fluid_loop_1", "loop": "HW_Loop_2", "type": "HOT_WATER"},
    ],
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__all_terminal_heating_loops_boiler():
    assert (
        are_all_terminal_heating_loops_attached_to_boiler(TEST_RMD, ["terminal_1"])
        == True
    )


def test__not_all_terminal_heating_source_boiler():
    assert (
        are_all_terminal_heating_loops_attached_to_boiler(TEST_RMD, ["terminal_2"])
        == False
    )


def test__not_all_terminal_heating_source_boiler_null():
    assert (
        are_all_terminal_heating_loops_attached_to_boiler(TEST_RMD, ["terminal_3"])
        == False
    )
