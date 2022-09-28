from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fan_configs_parallel import (
    are_all_terminal_fans_config_parallel,
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
                                {"id": "terminal_1", "fan_configuration": "PARALLEL"},
                                {"id": "terminal_2"},
                                {"id": "terminal_3", "fan_configuration": "SERIES"},
                            ],
                        },
                    ],
                }
            ],
        }
    ],
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__all_terminal_fans_parallel():
    assert are_all_terminal_fans_config_parallel(TEST_RMD, ["terminal_1"]) == True


def test__one_terminal_fans_none_parallel():
    assert (
        are_all_terminal_fans_config_parallel(
            TEST_RMD, ["terminal_1", "terminal_2", "terminal_3"]
        )
        == False
    )


def test__all_terminal_fans_null():
    assert are_all_terminal_fans_config_parallel(TEST_RMD, ["terminal_2"]) == False
