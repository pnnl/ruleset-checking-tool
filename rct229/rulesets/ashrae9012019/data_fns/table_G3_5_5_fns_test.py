from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_5_fns import table_G3_5_5_lookup
from rct229.schema.config import ureg


btu_h = ureg("btu_h")


# Testing table_3_5_5------------------------------------------
def test__table_3_5_5_furnace_220000():
    assert table_G3_5_5_lookup("Warm-air furnace, gas-fired", 220000 * btu_h) == [
        {
            "minimum_efficiency": 0.78,
            "efficiency_metric": "ANNUAL_FUEL_UTILIZATION_EFFICIENCY",
        },
        {"minimum_efficiency": 0.80, "efficiency_metric": "THERMAL_EFFICIENCY"},
    ]


def test__table_3_5_5_furnace_240000():
    assert table_G3_5_5_lookup("Warm-air furnace, gas-fired", 240000 * btu_h) == [
        {"minimum_efficiency": 0.80, "efficiency_metric": "COMBUSTION_EFFICIENCY"}
    ]


def test__table_3_5_5_uh():
    assert table_G3_5_5_lookup("Warm-air unit heaters, gas-fired", 240000 * btu_h) == [
        {"minimum_efficiency": 0.80, "efficiency_metric": "COMBUSTION_EFFICIENCY"}
    ]
