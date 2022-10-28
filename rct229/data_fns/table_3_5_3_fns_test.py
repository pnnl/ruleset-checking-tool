import pytest

from rct229.data_fns.table_3_5_3_fns import table_G3_5_3_lookup
from rct229.schema.config import ureg

kw_per_ton = ureg("kilowatt / ton")


# Testing table_3_5_3------------------------------------------
def test__table_3_5_3_screw_80():
    assert table_G3_5_3_lookup("SCREW", 80) == {
        "minimum_full_load_efficiency_kw_per_ton": 0.790 * kw_per_ton,
        "minimum_integrated_part_load_kw_per_ton": 0.676 * kw_per_ton,
    }


def test__table_3_5_3_screw_160():
    assert table_G3_5_3_lookup("SCREW", 160) == {
        "minimum_full_load_efficiency_kw_per_ton": 0.718 * kw_per_ton,
        "minimum_integrated_part_load_kw_per_ton": 0.629 * kw_per_ton,
    }


def test__table_3_5_3_screw_320():
    assert table_G3_5_3_lookup("SCREW", 320) == {
        "minimum_full_load_efficiency_kw_per_ton": 0.639 * kw_per_ton,
        "minimum_integrated_part_load_kw_per_ton": 0.572 * kw_per_ton,
    }


def test__table_3_5_3_centrifugal_80():
    assert table_G3_5_3_lookup("CENTRIFUGAL", 80) == {
        "minimum_full_load_efficiency_kw_per_ton": 0.703 * kw_per_ton,
        "minimum_integrated_part_load_kw_per_ton": 0.670 * kw_per_ton,
    }


def test__table_3_5_3_centrifugal_160():
    assert table_G3_5_3_lookup("CENTRIFUGAL", 160) == {
        "minimum_full_load_efficiency_kw_per_ton": 0.634 * kw_per_ton,
        "minimum_integrated_part_load_kw_per_ton": 0.596 * kw_per_ton,
    }


def test__table_3_5_3_centrifugal_320():
    assert table_G3_5_3_lookup("CENTRIFUGAL", 320) == {
        "minimum_full_load_efficiency_kw_per_ton": 0.576 * kw_per_ton,
        "minimum_integrated_part_load_kw_per_ton": 0.549 * kw_per_ton,
    }
