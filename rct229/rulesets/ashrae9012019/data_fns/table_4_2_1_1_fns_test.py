# Testing table_4_2_1_1------------------------------------------
from rct229.rulesets.ashrae9012019.data_fns.table_4_2_1_1_fns import (
    table_4_2_1_1_lookup,
)


def test__table_4_2_1_1_MULTIFAMILY_CZ0A():
    assert table_4_2_1_1_lookup("MULTIFAMILY", "CZ0A") == {
        "building_performance_factor": 0.68
    }


def test__table_4_2_1_1_HEALTHCARE_HOSPITAL_CZ1B():
    assert table_4_2_1_1_lookup("HEALTHCARE_HOSPITAL", "CZ1B") == {
        "building_performance_factor": 0.60
    }


def test__table_4_2_1_1_HEALTHCARE_HOSPITAL_CZ7():
    assert table_4_2_1_1_lookup("HEALTHCARE_HOSPITAL", "CZ7") == {
        "building_performance_factor": 0.57
    }


def test__table_4_2_1_1_HOTEL_MOTEL_CZ3A():
    assert table_4_2_1_1_lookup("HOTEL_MOTEL", "CZ3A") == {
        "building_performance_factor": 0.53
    }


def test__table_4_2_1_1_OFFICE_CZ4B():
    assert table_4_2_1_1_lookup("OFFICE", "CZ4B") == {
        "building_performance_factor": 0.52
    }


def test__table_4_2_1_1_RESTAURANT_CZ2A():
    assert table_4_2_1_1_lookup("RESTAURANT", "CZ2A") == {
        "building_performance_factor": 0.60
    }


def test__table_4_2_1_1_RETAIL_CZ5C():
    assert table_4_2_1_1_lookup("RETAIL", "CZ5C") == {
        "building_performance_factor": 0.55
    }


def test__table_4_2_1_1_SCHOOL_CZ4A():
    assert table_4_2_1_1_lookup("SCHOOL", "CZ4A") == {
        "building_performance_factor": 0.37
    }


def test__table_4_2_1_1_WAREHOUSE_CZ8():
    assert table_4_2_1_1_lookup("WAREHOUSE", "CZ8") == {
        "building_performance_factor": 0.57
    }


def test__table_4_2_1_1_ALL_OTHER_CZ6B():
    assert table_4_2_1_1_lookup("ALL_OTHER", "CZ6B") == {
        "building_performance_factor": 0.50
    }
