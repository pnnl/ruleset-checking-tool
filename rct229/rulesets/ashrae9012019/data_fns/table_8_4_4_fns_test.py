import pytest
from numpy.testing import assert_approx_equal
from rct229.rulesets.ashrae9012019.data_fns.table_8_4_4_fns import (
    SINGLE_PHASE,
    THREE_PHASE,
    table_8_4_4_in_range,
    table_8_4_4_lookup,
)
from rct229.schema.config import ureg

kVA = ureg("kilovolt * ampere")


# Testing table_8_4_4_in_range()
# Use these range values
# MIN_KVA = 15
# MAX_SINGLE_PHASE_KVA = 333
# MAX_THREE_PHASE_KVA = 1000
def test__table_8_4_4_in_range__with_single_phase_low_value():
    assert table_8_4_4_in_range(phase=SINGLE_PHASE, capacity=14 * kVA) == False


def test__table_8_4_4_in_range__with_three_phase_low_value():
    assert table_8_4_4_in_range(phase=THREE_PHASE, capacity=14 * kVA) == False


def test__table_8_4_4_in_range__with_single_phase_high_value():
    assert table_8_4_4_in_range(phase=SINGLE_PHASE, capacity=350 * kVA) == False


def test__table_8_4_4_in_range__with_three_phase_high_value():
    assert table_8_4_4_in_range(phase=THREE_PHASE, capacity=1100 * kVA) == False


def test__table_8_4_4_in_range__with_single_phase_in_range_value():
    assert table_8_4_4_in_range(phase=SINGLE_PHASE, capacity=100 * kVA) == True


def test__table_8_4_4_in_range__with_three_phase_in_range_value():
    assert table_8_4_4_in_range(phase=THREE_PHASE, capacity=800 * kVA) == True


# Testing table_8_4_4_lookup()
def test__test__table_8_4_4_lookup__with_single_phase_low_value():
    with pytest.raises(AssertionError, match="capacity out of range"):
        table_8_4_4_lookup(phase=SINGLE_PHASE, capacity=14 * kVA)


def test__test__table_8_4_4_lookup__with_three_phase_low_value():
    with pytest.raises(AssertionError, match="capacity out of range"):
        table_8_4_4_lookup(phase=THREE_PHASE, capacity=14 * kVA)


def test__test__table_8_4_4_lookup__with_single_phase_high_value():
    with pytest.raises(AssertionError, match="capacity out of range"):
        table_8_4_4_lookup(phase=SINGLE_PHASE, capacity=350 * kVA)


def test__test__table_8_4_4_lookup__with_three_phase_high_value():
    with pytest.raises(AssertionError, match="capacity out of range"):
        table_8_4_4_lookup(phase=THREE_PHASE, capacity=1100 * kVA)


def test__test__table_8_4_4_lookup__with_single_phase_in_range_value():
    assert table_8_4_4_lookup(phase=SINGLE_PHASE, capacity=75 * kVA) == {
        "efficiency": 0.985
    }


def test__test__table_8_4_4_lookup__with_three_phase_in_range_value():
    assert table_8_4_4_lookup(phase=THREE_PHASE, capacity=75 * kVA) == {
        "efficiency": 0.986
    }


def test__test__table_8_4_4_lookup__with_single_phase_between_values():
    assert_approx_equal(
        table_8_4_4_lookup(phase=SINGLE_PHASE, capacity=20 * kVA).get("efficiency"),
        (0.977 + 0.98) / 2,
    )
