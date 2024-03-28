import inspect

from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_1 import (
    SYS_1_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_2 import (
    SYS_2_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_3 import (
    SYS_3_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_4 import (
    SYS_4_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_5 import (
    SYS_5_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_6 import (
    SYS_6_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_7 import (
    SYS_7_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_8 import (
    SYS_8_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_9 import (
    SYS_9_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_10 import (
    SYS_10_FIRST_LOGIC_TEST_RMD,
    SYS_10_SECOND_LOGIC_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_11_1 import (
    SYS_11_1_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.test_is_baseline_system_11_2 import (
    SYS_11_2_TEST_RMD,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)


def exclude_sys_types(exclude_type: list[str]) -> list[str]:
    return [
        getattr(HVAC_SYS, sys_type[0])
        for sys_type in inspect.getmembers(HVAC_SYS)
        if sys_type[1] not in exclude_type
    ]


def available_type_lists(baseline_system_types_dict: dict) -> list:
    return [
        hvac_type
        for hvac_type in baseline_system_types_dict
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]


def test_get_baseline_system_types__system_1_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_1_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_1, HVAC_SYS.SYS_1A, HVAC_SYS.SYS_1B, HVAC_SYS.SYS_1C]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_1_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_1_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types(
        [
            HVAC_SYS.SYS_1,
            HVAC_SYS.SYS_1A,
            HVAC_SYS.SYS_1B,
            HVAC_SYS.SYS_1C,
        ]
    )
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_2_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_2_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_2]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_2_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_2_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types([HVAC_SYS.SYS_2])
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_3_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_3_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_3, HVAC_SYS.SYS_3A, HVAC_SYS.SYS_3B, HVAC_SYS.SYS_3C]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_3_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_3_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types(
        [
            HVAC_SYS.SYS_3,
            HVAC_SYS.SYS_3A,
            HVAC_SYS.SYS_3B,
            HVAC_SYS.SYS_3C,
        ]
    )
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_4_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_4_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_4]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_4_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_4_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types([HVAC_SYS.SYS_4])
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_5_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_5_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_5, HVAC_SYS.SYS_5B]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_5_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_5_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types([HVAC_SYS.SYS_5, HVAC_SYS.SYS_5B])
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_6_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_6_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_6, HVAC_SYS.SYS_6B]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_6_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_6_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types([HVAC_SYS.SYS_6, HVAC_SYS.SYS_6B])
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_7_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_7_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_7, HVAC_SYS.SYS_7A, HVAC_SYS.SYS_7B, HVAC_SYS.SYS_7C]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_7_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_7_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types(
        [HVAC_SYS.SYS_7, HVAC_SYS.SYS_7A, HVAC_SYS.SYS_7B, HVAC_SYS.SYS_7C]
    )
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_8_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_8_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_8, HVAC_SYS.SYS_8A, HVAC_SYS.SYS_8B, HVAC_SYS.SYS_8C]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_8_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_8_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types(
        [HVAC_SYS.SYS_8, HVAC_SYS.SYS_8A, HVAC_SYS.SYS_8B, HVAC_SYS.SYS_8C]
    )
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_9_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_9_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_9, HVAC_SYS.SYS_9B]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_9_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_9_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types([HVAC_SYS.SYS_9, HVAC_SYS.SYS_9B])
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_10_first_logic_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_10_FIRST_LOGIC_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_10]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_10_first_logic_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_10_FIRST_LOGIC_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types([HVAC_SYS.SYS_10])
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_10_second_logic_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_10_SECOND_LOGIC_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_10]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_10_second_logic_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_10_SECOND_LOGIC_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types([HVAC_SYS.SYS_10])
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_11_1_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_11_1_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [
        HVAC_SYS.SYS_11_1,
        HVAC_SYS.SYS_11_1A,
        HVAC_SYS.SYS_11_1B,
        HVAC_SYS.SYS_11_1C,
    ]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_11_1_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_11_1_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types(
        [
            HVAC_SYS.SYS_11_1,
            HVAC_SYS.SYS_11_1A,
            HVAC_SYS.SYS_11_1B,
            HVAC_SYS.SYS_11_1C,
        ]
    )
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )


def test_get_baseline_system_types__system_11_2_true():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_11_2_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = [HVAC_SYS.SYS_11_2, HVAC_SYS.SYS_11_2A]
    assert any(
        [
            available_type in test_types
            for available_type in available_type_lists(baseline_system_types_dict)
        ]
    )


def test_get_baseline_system_types__system_11_2_false():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_11_2_TEST_RMD["ruleset_model_descriptions"][0]
    )
    test_types = exclude_sys_types([HVAC_SYS.SYS_11_2, HVAC_SYS.SYS_11_2A])
    assert (
        any(
            [
                available_type in test_types
                for available_type in available_type_lists(baseline_system_types_dict)
            ]
        )
        == False
    )
