import pytest
import re
from rct229.rulesets.ashrae9012019.data_fns.table_7_8_fns import table_7_8_lookup
from rct229.schema.config import ureg
from rct229.utils.assertions import RCTFailureException


# Testing table_7_8------------------------------------------
def test__table_7_8_lookup_elec_under12kw():
    assert (
        table_7_8_lookup(
            "Electric storage water heater",
            11.9 * ureg.kilowatt,
        )
        == []
    )


def test__table_7_8_lookup_elec_over12kw():
    assert table_7_8_lookup("Electric storage water heater", 12.0 * ureg.kilowatt,) == [
        {
            "equation": "0.3 + 27/v",
            "metric": "STANDBY_LOSS_FRACTION",
        }
    ]


def test__table_7_8_lookup_gas_75kbtuh():
    assert (
        table_7_8_lookup(
            "Gas storage water heater",
            75.0 * ureg("kBtu/h"),
        )
        == []
    )


def test__table_7_8_lookup_gas_105kbtuh_low():
    assert table_7_8_lookup(
        "Gas storage water heater",
        105.0 * ureg("kBtu/h"),
        "Low",
    ) == [
        {
            "equation": "0.5362 - 0.0012*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_7_8_lookup_gas_105kbtuh_high():
    assert table_7_8_lookup(
        "Gas storage water heater",
        105.0 * ureg("kBtu/h"),
        "High",
    ) == [
        {
            "equation": "0.6597 - 0.0009*v",
            "metric": "UNIFORM_ENERGY_FACTOR",
        }
    ]


def test__table_7_8_lookup_gas_over105kbtuh():
    assert table_7_8_lookup("Gas storage water heater", 106.0 * ureg("kBtu/h"),) == [
        {
            "equation": "0.80",
            "metric": "THERMAL_EFFICIENCY",
        },
        {
            "equation": "q/800 + 110*v**0.5",
            "metric": "STANDBY_LOSS_ENERGY",
        },
    ]


def test__table_7_8_invalid_draw_pattern():
    expected_message = "Invalid draw pattern. Must be one of ['', 'Very small', 'Low', 'Medium', 'High']"
    with pytest.raises(AssertionError, match=re.escape(expected_message)):
        table_7_8_lookup("Gas storage water heater", 106.0 * ureg("kBtu/h"), "Invalid")


def test__table_7_8_invalid_equipment_type():
    expected_message = "Invalid equipment type. Must be one of ['Electric storage water heater', 'Gas storage water heater']"
    with pytest.raises(AssertionError, match=re.escape(expected_message)):
        table_7_8_lookup("Storage water heater", 106.0 * ureg("kBtu/h"), "High")
