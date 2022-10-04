import pytest

from rct229.data_fns.table_3_1_3_7_fns import table_3_1_3_7_lookup
from rct229.schema.config import ureg

degree_fahrenheit = ureg("degree_Fahrenheit")

# Testing table_3_1_3_7------------------------------------------
def test__table_3_1_3_7_CZ0A():
    assert table_3_1_3_7_lookup("CZ0A") == {
        "leaving_water_temperature": 80 * degree_fahrenheit
    }


def test__table_3_1_3_7_CZ0B():
    assert table_3_1_3_7_lookup("CZ0B") == {
        "leaving_water_temperature": 70 * degree_fahrenheit
    }


def test__table_3_1_3_7_CZ5C():
    assert table_3_1_3_7_lookup("CZ5C") == {
        "leaving_water_temperature": 65 * degree_fahrenheit
    }
