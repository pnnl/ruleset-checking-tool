from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_supplies_ducted import (
    are_all_terminal_supplies_ducted,
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
                                {"id": "terminal_1", "is_supply_ducted": True},
                                {"id": "terminal_2", "is_supply_ducted": False},
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


def test__all_terminal_supplies_ducted_true():
    assert are_all_terminal_supplies_ducted(TEST_RMD, ["terminal_1"]) == True


def test__all_terminal_supplies_ducted_false():
    assert are_all_terminal_supplies_ducted(TEST_RMD, ["terminal_2"]) == False


def test__all_terminal_supplies_ducted_null():
    assert are_all_terminal_supplies_ducted(TEST_RMD, ["terminal_3"]) == False
