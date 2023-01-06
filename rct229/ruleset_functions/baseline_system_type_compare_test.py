from rct229.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS


def test_baseline_system_type_compare_test_exact_match__matched():
    assert baseline_system_type_compare(HVAC_SYS.SYS_1, HVAC_SYS.SYS_1)


def test_baseline_system_type_compare_test_exact_match__mismatched():
    assert not baseline_system_type_compare(HVAC_SYS.SYS_1, HVAC_SYS.SYS_2)


def test_baseline_system_type_compare_test_not_exact_match__matched():
    assert baseline_system_type_compare(
        HVAC_SYS.SYS_1, HVAC_SYS.SYS_1C, exact_match=False
    )


def test_baseline_system_type_compare_test_not_exact_match__mismatched():
    assert not baseline_system_type_compare(
        HVAC_SYS.SYS_1, HVAC_SYS.SYS_2, exact_match=False
    )
