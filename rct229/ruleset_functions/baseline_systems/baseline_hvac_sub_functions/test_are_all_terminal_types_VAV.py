from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_VAV import (
    are_all_terminal_types_VAV,
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
                                {"id": "terminal_1", "type": "VARIABLE_AIR_VOLUME"},
                                {"id": "terminal_2", "type": "CONSTANT_AIR_VOLUME"},
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


def test__all_terminal_type_VAV():
    assert are_all_terminal_types_VAV(TEST_RMD, ["terminal_1"]) == True


def test__not_all_terminal_type_VAV():
    assert are_all_terminal_types_VAV(TEST_RMD, ["terminal_2"]) == False


def test__none_terminal_type_VAV():
    assert are_all_terminal_types_VAV(TEST_RMD, ["terminal_3"]) == False
