from rct229.rulesets.ashrae9012019.data_fns.table_7_8_fns import (
    table_7_8_lookup
)
from rct229.schema.config import ureg


# Testing table_7_8------------------------------------------
def test__table_7_8_lookup_elec_under12kw():
    assert table_7_8_lookup(
        "Electric storage water heater",
        11.9 * ureg.kilowatt,
    ) == []


def test__table_7_8_lookup_elec_over12kw():
    assert table_7_8_lookup(
        "Electric storage water heater",
        12.0 * ureg.kilowatt,
    ) == [
        {
            'Equipment Type': 'Electric storage water heater',
            'Capacity min': {'inclusive': True, 'unit': 'kW', 'value': 12},
            'Capacity max': {'inclusive': False, 'unit': 'kW', 'value': 9999},
            'Draw Pattern': '',
            'Efficiency': {
                'equation': '0.3 + 27/v_m',
                'metric': 'STANDBY_LOSS_FRACTION',
                'variables': ['v_m']
            },
        }
    ]


def test__table_7_8_lookup_gas_75kbtuh():
    assert table_7_8_lookup(
        "Gas storage water heater",
        75.0 * ureg("kBtu/h"),
    ) == []


def test__table_7_8_lookup_gas_105kbtuh_low():
    assert table_7_8_lookup(
        "Gas storage water heater",
        105.0 * ureg("kBtu/h"),
        "Low",
    ) == [
        {
            'Equipment Type': 'Gas storage water heater',
            'Capacity min': {'inclusive': False, 'unit': 'Btu/h', 'value': 75000},
            'Capacity max': {'inclusive': True, 'unit': 'Btu/h', 'value': 105000},
            'Draw Pattern': 'Low',
            'Efficiency': {
                'equation': '0.5362 - 0.0012*v_r',
                'metric': 'UNIFORM_ENERGY_FACTOR',
                'variables': ['v_r']
            },
         }
    ]


def test__table_7_8_lookup_gas_105kbtuh_high():
    assert table_7_8_lookup(
        "Gas storage water heater",
        105.0 * ureg("kBtu/h"),
        "High",
    ) == [
        {
            'Equipment Type': 'Gas storage water heater',
            'Capacity min': {'inclusive': False, 'unit': 'Btu/h', 'value': 75000},
            'Capacity max': {'inclusive': True, 'unit': 'Btu/h', 'value': 105000},
            'Draw Pattern': 'High',
            'Efficiency': {
                'equation': '0.6597 - 0.0009*v_r',
                'metric': 'UNIFORM_ENERGY_FACTOR',
                'variables': ['v_r']
            },
         }
    ]


def test__table_7_8_lookup_gas_over105kbtuh():
    assert table_7_8_lookup(
        "Gas storage water heater",
        106.0 * ureg("kBtu/h"),
    ) == [
        {
            'Equipment Type': 'Gas storage water heater',
            'Capacity min': {'inclusive': False, 'unit': 'Btu/h', 'value': 105000},
            'Capacity max': {'inclusive': True, 'unit': 'Btu/h', 'value': 9999999},
            'Draw Pattern': '',
            'Efficiency': {
                'equation': '0.80',
                'metric': 'THERMAL_EFFICIENCY',
                'variables': []
            },
         },
        {
            'Equipment Type': 'Gas storage water heater',
            'Capacity min': {'inclusive': False, 'unit': 'Btu/h', 'value': 105000},
            'Capacity max': {'inclusive': True, 'unit': 'Btu/h', 'value': 9999999},
            'Draw Pattern': '',
            'Efficiency': {
                'equation': 'q/800 + 110*v**0.5',
                'metric': 'STANDBY_LOSS_ENERGY',
                'variables': ['q', 'v']
            },
        }
    ]




