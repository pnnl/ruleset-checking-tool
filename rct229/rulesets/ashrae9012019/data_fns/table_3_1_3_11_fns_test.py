from rct229.rulesets.ashrae9012019.data_fns.table_3_1_3_11_fns import (
    table_3_1_3_11_lookup,
)
from rct229.schema.config import ureg

degree_fahrenheit = ureg("degree_Fahrenheit")


# Testing table_3_1_3_7------------------------------------------
def test__table_3_1_3_11_CZ0A():
    assert table_3_1_3_11_lookup("CZ0A") == {
        "leaving_water_temperature": ureg("80 degree_Fahrenheit")
    }


def test__table_3_1_3_11_CZ0B():
    assert table_3_1_3_11_lookup("CZ0B") == {
        "leaving_water_temperature": ureg("70 degree_Fahrenheit")
    }


def test__table_3_1_3_11_CZ5C():
    assert table_3_1_3_11_lookup("CZ5C") == {
        "leaving_water_temperature": ureg("65 degree_Fahrenheit")
    }
