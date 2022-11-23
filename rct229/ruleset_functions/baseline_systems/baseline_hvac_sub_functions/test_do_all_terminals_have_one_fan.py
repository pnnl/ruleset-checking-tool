
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.do_all_terminals_have_one_fan import \
    do_all_terminals_have_one_fan

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
                                {"id": "terminal_1", "fan": "fan_1"},
                                {"id": "terminal_2"},
                                {"id": "terminal_3", "fan": "fan_2"},
                            ],
                        },
                    ],
                }
            ],
        }
    ],
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__do_all_terminals_have_one_fan__all_have():
    assert do_all_terminals_have_one_fan(TEST_RMD, ["terminal_1", "terminal_3"]) == True


def test__do_all_terminals_have_one_fan__not_all_have():
    assert (
        do_all_terminals_have_one_fan(TEST_RMD, ["terminal_1", "terminal_2", "terminal_3"])
        == False
    )


def test__do_all_terminals_have_one_fan__none_have():
    assert do_all_terminals_have_one_fan(TEST_RMD, ["terminal_2"]) == False
