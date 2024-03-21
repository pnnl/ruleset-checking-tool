from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_5_fns import table_g3_5_5_lookup


# Testing table_3_5_5------------------------------------------
def test__table_3_5_5_furnace_0():
    assert table_g3_5_5_lookup("Warm-air furnace, gas-fired", 0) == [
        {
            "minimum_efficiency": 0.78,
            "efficiency_metric": "ANNUAL_FUEL_UTILIZATION_EFFICIENCY",
            "most_conservative_efficiency": None,
        },
        {
            "minimum_efficiency": 0.80,
            "efficiency_metric": "THERMAL_EFFICIENCY",
            "most_conservative_efficiency": None,
        },
    ]


def test__table_3_5_5_furnace_224999():
    assert table_g3_5_5_lookup("Warm-air furnace, gas-fired", 224999) == [
        {
            "minimum_efficiency": 0.78,
            "efficiency_metric": "ANNUAL_FUEL_UTILIZATION_EFFICIENCY",
            "most_conservative_efficiency": None,
        },
        {
            "minimum_efficiency": 0.80,
            "efficiency_metric": "THERMAL_EFFICIENCY",
            "most_conservative_efficiency": None,
        },
    ]


def test__table_3_5_5_furnace_225000():
    assert table_g3_5_5_lookup("Warm-air furnace, gas-fired", 225000) == [
        {
            "minimum_efficiency": 0.80,
            "efficiency_metric": "COMBUSTION_EFFICIENCY",
            "most_conservative_efficiency": None,
        }
    ]


def test__table_3_5_5_uh():
    assert table_g3_5_5_lookup("Warm-air unit heaters, gas-fired", 240000) == [
        {
            "minimum_efficiency": 0.80,
            "efficiency_metric": "COMBUSTION_EFFICIENCY",
            "most_conservative_efficiency": None,
        }
    ]
