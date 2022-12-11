from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_7 import (
    SYS_7_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_11_1 import (
    SYS_11_1_TEST_RMD,
)
from rct229.ruleset_functions.baseline_systems.test_is_baseline_system_11_2 import (
    SYS_11_2_TEST_RMD,
)
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types


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
