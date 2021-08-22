import pytest
from rct229.data_fns.table_G3_8_fns import (
    lighting_space_enumeration_to_lpd_space_type_map,
    table_G3_8_lpd,
)


# Testing table_G3_8_lpd() ------------------------------------------
def test_table_G3_8_lpd_automotive_facility():
    assert table_G3_8_lpd("AUTOMOTIVE_FACILITY") == 0.9


def test_table_G3_8_lpd_convention_center():
    assert table_G3_8_lpd("CONVENTION_CENTER") == 1.20


def test_table_G3_8_lpd_courthouse():
    assert table_G3_8_lpd("COURTHOUSE") == 1.20


def test_table_G3_8_lpd_workshop():
    assert table_G3_8_lpd("WORKSHOP") == 1.40


def test_table_G3_8_lpd_warehouse():
    assert table_G3_8_lpd("WAREHOUSE") == 0.80


def test_table_G3_8_lpd_courthouse():
    assert table_G3_8_lpd("COURTHOUSE") == 1.20
