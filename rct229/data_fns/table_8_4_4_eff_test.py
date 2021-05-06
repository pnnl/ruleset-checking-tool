import pytest
from table_8_4_4_eff import (
    SINGLE_PHASE,
    THREE_PHASE,
    table_8_4_4_eff,
    table_8_4_4_in_range,
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


# Testing table_8_4_4_eff()
def test__table_8_4_4_eff__with_single_phase_low_value():
    with pytest.raises(ValueError, match="kVA out of range"):
        table_8_4_4_eff(phase=SINGLE_PHASE, kVA=14)


def test__table_8_4_4_eff__with_three_phase_low_value():
    with pytest.raises(ValueError, match="kVA out of range"):
        table_8_4_4_eff(phase=THREE_PHASE, kVA=14)


def test__table_8_4_4_eff__with_single_phase_high_value():
    with pytest.raises(ValueError, match="kVA out of range"):
        table_8_4_4_eff(phase=SINGLE_PHASE, kVA=350)


def test__table_8_4_4_eff__with_three_phase_high_value():
    with pytest.raises(ValueError, match="kVA out of range"):
        table_8_4_4_eff(phase=THREE_PHASE, kVA=1100)


def test__table_8_4_4_eff__with_single_phase_in_range_value():
    assert table_8_4_4_eff(phase=SINGLE_PHASE, kVA=75) == 98.5


def test__table_8_4_4_eff__with_three_phase_in_range_value():
    assert table_8_4_4_eff(phase=THREE_PHASE, kVA=75) == 98.6


def test__table_8_4_4_eff__with_single_phase_between_values():
    assert table_8_4_4_eff(phase=SINGLE_PHASE, kVA=20) == (97.7 + 98) / 2
