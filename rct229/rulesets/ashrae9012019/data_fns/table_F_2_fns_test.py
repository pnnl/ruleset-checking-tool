import pytest
import re
from rct229.rulesets.ashrae9012019.data_fns.table_F_2_fns import table_f_2_lookup
from rct229.schema.config import ureg
from rct229.utils.assertions import RCTFailureException


# Testing 90.1 Appendix F Table F-2------------------------------------------
def test__table_f_2_lookup_gas_under20gal():
    assert (
        table_f_2_lookup(
            "Gas storage water heater",
            19.9 * ureg.gallon,
            "Very small",
        )
        == []
    )


def test__table_f_2_lookup_gas_20to55gal_low():
    assert table_f_2_lookup("Gas storage water heater", 20.0 * ureg.gallon, "Low") == [
        {
            "equation": "0.5982 - 0.0019*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_f_2_lookup_gas_20to55gal_high():
    assert table_f_2_lookup("Gas storage water heater", 55.0 * ureg.gallon, "High") == [
        {
            "equation": "0.6920 - 0.0013*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_f_2_lookup_gas_55to100gal_low():
    assert table_f_2_lookup("Gas storage water heater", 55.1 * ureg.gallon, "Low") == [
        {
            "equation": "0.7689 - 0.0005*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_f_2_lookup_gas_55to100gal_high():
    assert table_f_2_lookup("Gas storage water heater", 100 * ureg.gallon, "High") == [
        {
            "equation": "0.8072 - 0.0003*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_f_2_lookup_gas_over100gal():
    assert (
        table_f_2_lookup(
            "Gas storage water heater",
            100.1 * ureg.gallon,
            "Very small",
        )
        == []
    )


def test__table_f_2_lookup_elec_under20gal():
    assert (
        table_f_2_lookup(
            "Electric storage water heater",
            19.9 * ureg.gallon,
            "Very small",
        )
        == []
    )


def test__table_f_2_lookup_elec_20to55gal_low():
    assert table_f_2_lookup(
        "Electric storage water heater", 20.0 * ureg.gallon, "Low"
    ) == [
        {
            "equation": "0.9254 - 0.0003*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_f_2_lookup_elec_20to55gal_high():
    assert table_f_2_lookup(
        "Electric storage water heater", 55.0 * ureg.gallon, "High"
    ) == [
        {
            "equation": "0.9349 - 0.0001*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_f_2_lookup_elec_55to100gal_low():
    assert table_f_2_lookup(
        "Electric storage water heater", 55.1 * ureg.gallon, "Low"
    ) == [
        {
            "equation": "2.0440 - 0.0011*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_f_2_lookup_elec_55to100gal_high():
    assert table_f_2_lookup(
        "Electric storage water heater", 100 * ureg.gallon, "High"
    ) == [
        {
            "equation": "2.2418 - 0.0011*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_f_2_lookup_elec_over100gal():
    assert (
        table_f_2_lookup(
            "Electric storage water heater",
            100.1 * ureg.gallon,
            "Very small",
        )
        == []
    )


def test__table_7_8_invalid_draw_pattern():
    expected_message = (
        "Invalid draw pattern. Must be one of ['Very small', 'Low', 'Medium', 'High']"
    )
    with pytest.raises(AssertionError, match=re.escape(expected_message)):
        table_f_2_lookup("Gas storage water heater", 106.0 * ureg("kBtu/h"), "Invalid")


def test__table_7_8_invalid_equipment_type():
    expected_message = "Invalid equipment type. Must be one of ['Electric storage water heater', 'Gas storage water heater']"
    with pytest.raises(AssertionError, match=re.escape(expected_message)):
        table_f_2_lookup("Storage water heater", 106.0 * ureg("kBtu/h"), "High")
