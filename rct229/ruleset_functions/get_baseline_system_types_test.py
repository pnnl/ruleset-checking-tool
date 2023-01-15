from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_1 import (
    SYS_1_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_2 import (
    SYS_2_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_3 import (
    SYS_3_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_4 import (
    SYS_4_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_5 import (
    SYS_5_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_6 import (
    SYS_6_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_7 import (
    SYS_7_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_8 import (
    SYS_8_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_10 import (
    SYS_10_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_11_1 import (
    SYS_11_1_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_11_2 import (
    SYS_11_2_TEST_RMD,
)
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types


def test_get_baseline_system_types__system_1():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_1_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_types_dict.keys()
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_1, HVAC_SYS.SYS_1A, HVAC_SYS.SYS_1B, HVAC_SYS.SYS_1C]

    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_2():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_2_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_types_dict.keys()
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_2]

    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_3():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_3_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_types_dict.keys()
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_3, HVAC_SYS.SYS_3A, HVAC_SYS.SYS_3B, HVAC_SYS.SYS_3C]

    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_4():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_4_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_types_dict.keys()
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_4]

    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_5():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_5_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_types_dict.keys()
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_5, HVAC_SYS.SYS_5B]

    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_6():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_6_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_types_dict.keys()
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_6, HVAC_SYS.SYS_6B]

    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_7():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_7_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_types_dict.keys()
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_7, HVAC_SYS.SYS_7A, HVAC_SYS.SYS_7B, HVAC_SYS.SYS_7C]

    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_8():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_8_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_types_dict.keys()
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_8, HVAC_SYS.SYS_8A, HVAC_SYS.SYS_8B, HVAC_SYS.SYS_8C]

    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_10():
    baseline_system_types_dict = get_baseline_system_types(
        SYS_10_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_types_dict.keys()
        if len(baseline_system_types_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_10]

    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_11_1():
    baseline_system_type_dict = get_baseline_system_types(
        SYS_11_1_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_type_dict.keys()
        if len(baseline_system_type_dict[hvac_type]) > 0
    ]

    test_types = [
        HVAC_SYS.SYS_11_1,
        HVAC_SYS.SYS_11_1A,
        HVAC_SYS.SYS_11_1B,
        HVAC_SYS.SYS_11_1C,
    ]
    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )


def test_get_baseline_system_types__system_11_2():
    baseline_system_type_dict = get_baseline_system_types(
        SYS_11_2_TEST_RMD["ruleset_model_instances"][0]
    )
    available_type_lists = [
        hvac_type
        for hvac_type in baseline_system_type_dict.keys()
        if len(baseline_system_type_dict[hvac_type]) > 0
    ]

    test_types = [HVAC_SYS.SYS_11_2, HVAC_SYS.SYS_11_2A]
    assert any(
        [available_type in test_types for available_type in available_type_lists]
    )
