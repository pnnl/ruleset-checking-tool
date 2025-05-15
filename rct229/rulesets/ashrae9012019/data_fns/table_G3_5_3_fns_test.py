from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_3_fns import table_g3_5_3_lookup
from rct229.schema.config import ureg

ton = ureg("ton")
kw_per_ton = ureg("kilowatt / ton")


# Testing table_3_5_3------------------------------------------
def test__table_3_5_3_screw_0():
    assert table_g3_5_3_lookup("SCREW", 0 * ton) == {
        "minimum_full_load_efficiency": 0.790 * kw_per_ton,
        "minimum_integrated_part_load": 0.676 * kw_per_ton,
    }


def test__table_3_5_3_screw_149():
    assert table_g3_5_3_lookup("SCREW", 149 * ton) == {
        "minimum_full_load_efficiency": 0.790 * kw_per_ton,
        "minimum_integrated_part_load": 0.676 * kw_per_ton,
    }


def test__table_3_5_3_screw_150():
    assert table_g3_5_3_lookup("SCREW", 150 * ton) == {
        "minimum_full_load_efficiency": 0.718 * kw_per_ton,
        "minimum_integrated_part_load": 0.629 * kw_per_ton,
    }


def test__table_3_5_3_screw_320():
    assert table_g3_5_3_lookup("SCREW", 320 * ton) == {
        "minimum_full_load_efficiency": 0.639 * kw_per_ton,
        "minimum_integrated_part_load": 0.572 * kw_per_ton,
    }


def test__table_3_5_3_centrifugal_0():
    assert table_g3_5_3_lookup("CENTRIFUGAL", 0 * ton) == {
        "minimum_full_load_efficiency": 0.703 * kw_per_ton,
        "minimum_integrated_part_load": 0.670 * kw_per_ton,
    }


def test__table_3_5_3_centrifugal_149():
    assert table_g3_5_3_lookup("CENTRIFUGAL", 149 * ton) == {
        "minimum_full_load_efficiency": 0.703 * kw_per_ton,
        "minimum_integrated_part_load": 0.670 * kw_per_ton,
    }


def test__table_3_5_3_centrifugal_150():
    assert table_g3_5_3_lookup("CENTRIFUGAL", 150 * ton) == {
        "minimum_full_load_efficiency": 0.634 * kw_per_ton,
        "minimum_integrated_part_load": 0.596 * kw_per_ton,
    }


def test__table_3_5_3_centrifugal_320():
    assert table_g3_5_3_lookup("CENTRIFUGAL", 320 * ton) == {
        "minimum_full_load_efficiency": 0.576 * kw_per_ton,
        "minimum_integrated_part_load": 0.549 * kw_per_ton,
    }
