import pytest
from rct229.rulesets.ashrae9012022.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.utils.assertions import RCTException, RCTFailureException


def test_baseline_system_type_compare_test_exact_match__exception_sys_type():
    with pytest.raises(
        RCTFailureException,
        match="Not_Sys does not match any primary baseline HVAC system type",
    ):
        assert baseline_system_type_compare("SYS123", HVAC_SYS.UNMATCHED)


def test_baseline_system_type_compare_test_exact_match__exception_target_sys_type():
    with pytest.raises(
        RCTException,
        match="Sys-1a does not match any primary baseline HVAC system type",
    ):
        baseline_system_type_compare(HVAC_SYS.SYS_1, HVAC_SYS.SYS_1A)


def test_baseline_system_type_compare_test_exact_match__matched():
    assert baseline_system_type_compare(HVAC_SYS.SYS_1, HVAC_SYS.SYS_1)


def test_baseline_system_type_compare_test_exact_match__mismatched():
    assert not baseline_system_type_compare(HVAC_SYS.SYS_1, HVAC_SYS.SYS_2)


def test_baseline_system_type_compare_test_not_exact_match__matched():
    assert baseline_system_type_compare(
        HVAC_SYS.SYS_1C, HVAC_SYS.SYS_1, exact_match=False
    )


def test_baseline_system_type_compare_test_not_exact_match__mismatched():
    assert not baseline_system_type_compare(
        HVAC_SYS.SYS_1, HVAC_SYS.SYS_2, exact_match=False
    )
