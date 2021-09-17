import pytest
from numpy.testing import assert_approx_equal

from rct229.data_fns.table_8_4_4_fns import (
    SINGLE_PHASE,
    THREE_PHASE,
    table_8_4_4_in_range,
    table_8_4_4_lookup,
)


# Testing table_8_4_4_in_range()
# Use these range values
# MIN_KVA = 15
# MAX_SINGLE_PHASE_KVA = 333
# MAX_THREE_PHASE_KVA = 1000
def test__table_8_4_4_in_range__with_single_phase_low_value():
    assert table_8_4_4_in_range(phase=SINGLE_PHASE, kVA=14) == False


def test__table_8_4_4_in_range__with_three_phase_low_value():
    assert table_8_4_4_in_range(phase=THREE_PHASE, kVA=14) == False


def test__table_8_4_4_in_range__with_single_phase_high_value():
    assert table_8_4_4_in_range(phase=SINGLE_PHASE, kVA=350) == False


def test__table_8_4_4_in_range__with_three_phase_high_value():
    assert table_8_4_4_in_range(phase=THREE_PHASE, kVA=1100) == False


def test__table_8_4_4_in_range__with_single_phase_in_range_value():
    assert table_8_4_4_in_range(phase=SINGLE_PHASE, kVA=100) == True


def test__table_8_4_4_in_range__with_three_phase_in_range_value():
    assert table_8_4_4_in_range(phase=THREE_PHASE, kVA=800) == True


# Testing table_8_4_4_lookup()
def test__table_8_4_4_eff__with_single_phase_low_value():
    with pytest.raises(AssertionError, match="kVA out of range"):
        table_8_4_4_lookup(phase=SINGLE_PHASE, kVA=14)


def test__table_8_4_4_eff__with_three_phase_low_value():
    with pytest.raises(AssertionError, match="kVA out of range"):
        table_8_4_4_lookup(phase=THREE_PHASE, kVA=14)


def test__table_8_4_4_eff__with_single_phase_high_value():
    with pytest.raises(AssertionError, match="kVA out of range"):
        table_8_4_4_lookup(phase=SINGLE_PHASE, kVA=350)


def test__table_8_4_4_eff__with_three_phase_high_value():
    with pytest.raises(AssertionError, match="kVA out of range"):
        table_8_4_4_lookup(phase=THREE_PHASE, kVA=1100)


def test__table_8_4_4_eff__with_single_phase_in_range_value():
    assert table_8_4_4_lookup(phase=SINGLE_PHASE, kVA=75) == {"efficiency": 0.985}


def test__table_8_4_4_eff__with_three_phase_in_range_value():
    assert table_8_4_4_lookup(phase=THREE_PHASE, kVA=75) == {"efficiency": 0.986}


def test__table_8_4_4_eff__with_single_phase_between_values():
    assert_approx_equal(
        table_8_4_4_lookup(phase=SINGLE_PHASE, kVA=20).get("efficiency"),
        (0.977 + 0.98) / 2,
    )
