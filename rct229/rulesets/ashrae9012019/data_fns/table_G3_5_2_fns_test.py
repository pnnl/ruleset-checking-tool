from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_2_fns import table_G3_5_2_lookup
from rct229.schema.config import ureg

btu_h = ureg("btu_h")


# Testing table_3_5_2------------------------------------------
def test__table_3_5_2_cooling_60000():
    assert table_G3_5_2_lookup(
        "heat pumps, air-cooled (cooling mode)", "single-package", 60000 * btu_h
    ) == {
        "minimum_efficiency_copnf": 3.0,
    }


def test__table_3_5_2_cooling_90000():
    assert table_G3_5_2_lookup(
        "heat pumps, air-cooled (cooling mode)", "single-package", 90000 * btu_h
    ) == {
        "minimum_efficiency_copnf": 3.4,
    }


def test__table_3_5_2_cooling_180000():
    assert table_G3_5_2_lookup(
        "heat pumps, air-cooled (cooling mode)", "single-package", 180000 * btu_h
    ) == {
        "minimum_efficiency_copnf": 3.2,
    }


def test__table_3_5_2_cooling_360000():
    assert table_G3_5_2_lookup(
        "heat pumps, air-cooled (cooling mode)", "single-package", 360000 * btu_h
    ) == {
        "minimum_efficiency_copnf": 3.1,
    }


def test__table_3_5_2_heating_pkg_60000():
    assert table_G3_5_2_lookup(
        "heat pumps, air-cooled (heating mode)", "single-package", 60000 * btu_h
    ) == {
        "minimum_efficiency_copnf": 3.4,
    }


def test__table_3_5_2_heating_47_90000():
    assert table_G3_5_2_lookup(
        "heat pumps, air-cooled (heating mode)", "47F db/43F wb", 90000 * btu_h
    ) == {
        "minimum_efficiency_copnf": 3.4,
    }


def test__table_3_5_2_heating_17_90000():
    assert table_G3_5_2_lookup(
        "heat pumps, air-cooled (heating mode)", "17F db/15F wb", 90000 * btu_h
    ) == {
        "minimum_efficiency_copnf": 2.3,
    }


def test__table_3_5_2_heating_47_180000():
    assert table_G3_5_2_lookup(
        "heat pumps, air-cooled (heating mode)", "47F db/43F wb", 180000 * btu_h
    ) == {
        "minimum_efficiency_copnf": 3.4,
    }


def test__table_3_5_2_heating_17_180000():
    assert table_G3_5_2_lookup(
        "heat pumps, air-cooled (heating mode)", "17F db/15F wb", 180000 * btu_h
    ) == {
        "minimum_efficiency_copnf": 2.1,
    }