from rct229.rulesets.ashrae9012022.ruleset_functions.is_chiller_performance_app_j import (
    is_chiller_performance_app_j,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "RMD 1",
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "terminals": [
                                {
                                    "id": "VAV Air Terminal 1",
                                    "is_supply_ducted": True,
                                    "type": "VARIABLE_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                    "heating_source": "HOT_WATER",
                                    "heating_from_loop": "Boiler Loop 1",
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "terminals": [
                                {
                                    "id": "VAV Air Terminal 2",
                                    "is_supply_ducted": True,
                                    "type": "VARIABLE_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                    "heating_source": "HOT_WATER",
                                    "heating_from_loop": "Boiler Loop 1",
                                }
                            ],
                        },
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 7",
                            "cooling_system": {
                                "id": "CHW Coil 1",
                                "type": "FLUID_LOOP",
                                "chilled_water_loop": "Secondary CHW Loop 1",
                            },
                            "preheat_system": {
                                "id": "Preheat Coil 1",
                                "type": "FLUID_LOOP",
                                "hot_water_loop": "Boiler Loop 1",
                            },
                            "fan_system": {
                                "id": "VAV Fan System 1",
                                "fan_control": "VARIABLE_SPEED_DRIVE",
                                "supply_fans": [{"id": "Supply Fan 1"}],
                                "return_fans": [{"id": "Return Fan 1"}],
                            },
                        }
                    ],
                }
            ],
        }
    ],
    "boilers": [
        {"id": "Boiler 1", "loop": "Boiler Loop 1", "energy_source_type": "NATURAL_GAS"}
    ],
    "chillers": [
        {
            "id": "Chiller 1",
            "cooling_loop": "Chiller Loop 1",
            "compressor_type": "CENTRIFUGAL",
            "rated_capacity": 527550.0,
            "condensing_loop": "Condenser Loop 1",
            "efficiency_metric_values": [5.5],
            "efficiency_metric_types": ["FULL_LOAD_EFFICIENCY_RATED"],
            "capacity_operating_points": [
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 15.5555555555556,
                    "capacity": 522221.2,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 22.500000000000057,
                    "capacity": 360333,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 29.444444444444457,
                    "capacity": 349216,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 36.388888888888914,
                    "capacity": 336763,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 40.00000000000006,
                    "capacity": 417000.315,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 15.5555555555556,
                    "capacity": 358539,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 22.500000000000057,
                    "capacity": 348758,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 29.444444444444457,
                    "capacity": 337641,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 36.388888888888914,
                    "capacity": 325188,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 40.00000000000006,
                    "capacity": 317423,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 15.5555555555556,
                    "capacity": 345663,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 22.500000000000057,
                    "capacity": 335882,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 29.444444444444457,
                    "capacity": 324765,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 36.388888888888914,
                    "capacity": 312312,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 40.00000000000006,
                    "capacity": 304547,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 15.5555555555556,
                    "capacity": 331486,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 22.500000000000057,
                    "capacity": 321705,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 29.444444444444457,
                    "capacity": 310588,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 36.388888888888914,
                    "capacity": 298135,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 40.00000000000006,
                    "capacity": 290370,
                },
            ],
            "power_operating_points": [
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 15.5555555555556,
                    "load": 87925.0,
                    "power": 55019,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 15.5555555555556,
                    "load": 175850.0,
                    "power": 77828,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 15.5555555555556,
                    "load": 263775.0,
                    "power": 100637,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 15.5555555555556,
                    "load": 351700.0,
                    "power": 123446,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 22.500000000000057,
                    "load": 87925.0,
                    "power": 81486,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 22.500000000000057,
                    "load": 175850.0,
                    "power": 115280,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 22.500000000000057,
                    "load": 263775.0,
                    "power": 149074,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 22.500000000000057,
                    "load": 351700.0,
                    "power": 182868,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 29.444444444444457,
                    "load": 87925.0,
                    "power": 107867,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 29.444444444444457,
                    "load": 175850.0,
                    "power": 152616,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 29.444444444444457,
                    "load": 263775.0,
                    "power": 197365,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 29.444444444444457,
                    "load": 351700.0,
                    "power": 242114,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 36.388888888888914,
                    "load": 87925.0,
                    "power": 134316,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 36.388888888888914,
                    "load": 175850.0,
                    "power": 190020,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 36.388888888888914,
                    "load": 263775.0,
                    "power": 245724,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 36.388888888888914,
                    "load": 351700.0,
                    "power": 301428,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 40.00000000000006,
                    "load": 87925.0,
                    "power": 151006,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 40.00000000000006,
                    "load": 175850.0,
                    "power": 213695,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 40.00000000000006,
                    "load": 263775.0,
                    "power": 276384,
                },
                {
                    "chilled_water_supply_temperature": 3.888888888888914,
                    "condenser_temperature": 40.00000000000006,
                    "load": 351700.0,
                    "power": 339073,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 15.5555555555556,
                    "load": 87925.0,
                    "power": 61435,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 15.5555555555556,
                    "load": 175850.0,
                    "power": 86959,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 15.5555555555556,
                    "load": 263775.0,
                    "power": 112483,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 15.5555555555556,
                    "load": 351700.0,
                    "power": 138007,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 22.500000000000057,
                    "load": 87925.0,
                    "power": 82089,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 22.500000000000057,
                    "load": 175850.0,
                    "power": 116199,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 22.500000000000057,
                    "load": 263775.0,
                    "power": 150309,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 22.500000000000057,
                    "load": 351700.0,
                    "power": 184419,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 29.444444444444457,
                    "load": 87925.0,
                    "power": 102780,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 29.444444444444457,
                    "load": 175850.0,
                    "power": 145487,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 29.444444444444457,
                    "load": 263775.0,
                    "power": 188194,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 29.444444444444457,
                    "load": 351700.0,
                    "power": 230901,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 36.388888888888914,
                    "load": 87925.0,
                    "power": 123508,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 36.388888888888914,
                    "load": 175850.0,
                    "power": 174812,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 36.388888888888914,
                    "load": 263775.0,
                    "power": 226116,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 36.388888888888914,
                    "load": 351700.0,
                    "power": 277420,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 40.00000000000006,
                    "load": 87925.0,
                    "power": 136670,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 40.00000000000006,
                    "load": 175850.0,
                    "power": 193502,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 40.00000000000006,
                    "load": 263775.0,
                    "power": 250334,
                },
                {
                    "chilled_water_supply_temperature": 7.222222222222285,
                    "condenser_temperature": 40.00000000000006,
                    "load": 351700.0,
                    "power": 307166,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 15.5555555555556,
                    "load": 87925.0,
                    "power": 71585,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 15.5555555555556,
                    "load": 175850.0,
                    "power": 101313,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 15.5555555555556,
                    "load": 263775.0,
                    "power": 131041,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 15.5555555555556,
                    "load": 351700.0,
                    "power": 160769,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 22.500000000000057,
                    "load": 87925.0,
                    "power": 89197,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 22.500000000000057,
                    "load": 175850.0,
                    "power": 126234,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 22.500000000000057,
                    "load": 263775.0,
                    "power": 163271,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 22.500000000000057,
                    "load": 351700.0,
                    "power": 200308,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 29.444444444444457,
                    "load": 87925.0,
                    "power": 106846,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 29.444444444444457,
                    "load": 175850.0,
                    "power": 151193,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 29.444444444444457,
                    "load": 263775.0,
                    "power": 195540,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 29.444444444444457,
                    "load": 351700.0,
                    "power": 239887,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 36.388888888888914,
                    "load": 87925.0,
                    "power": 124532,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 36.388888888888914,
                    "load": 175850.0,
                    "power": 176189,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 36.388888888888914,
                    "load": 263775.0,
                    "power": 227846,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 36.388888888888914,
                    "load": 351700.0,
                    "power": 279503,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 40.00000000000006,
                    "load": 87925.0,
                    "power": 135953,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 40.00000000000006,
                    "load": 175850.0,
                    "power": 192407,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 40.00000000000006,
                    "load": 263775.0,
                    "power": 248861,
                },
                {
                    "chilled_water_supply_temperature": 10.000000000000057,
                    "condenser_temperature": 40.00000000000006,
                    "load": 351700.0,
                    "power": 305315,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 15.5555555555556,
                    "load": 87925.0,
                    "power": 81472,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 15.5555555555556,
                    "load": 175850.0,
                    "power": 115332,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 15.5555555555556,
                    "load": 263775.0,
                    "power": 149192,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 15.5555555555556,
                    "load": 351700.0,
                    "power": 183052,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 22.500000000000057,
                    "load": 87925.0,
                    "power": 96456,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 22.500000000000057,
                    "load": 175850.0,
                    "power": 136508,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 22.500000000000057,
                    "load": 263775.0,
                    "power": 176560,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 22.500000000000057,
                    "load": 351700.0,
                    "power": 216612,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 29.444444444444457,
                    "load": 87925.0,
                    "power": 111478,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 29.444444444444457,
                    "load": 175850.0,
                    "power": 157722,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 29.444444444444457,
                    "load": 263775.0,
                    "power": 203966,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 29.444444444444457,
                    "load": 351700.0,
                    "power": 250210,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 36.388888888888914,
                    "load": 87925.0,
                    "power": 126537,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 36.388888888888914,
                    "load": 175850.0,
                    "power": 179074,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 36.388888888888914,
                    "load": 263775.0,
                    "power": 231611,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 36.388888888888914,
                    "load": 351700.0,
                    "power": 284148,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 40.00000000000006,
                    "load": 87925.0,
                    "power": 136465,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 40.00000000000006,
                    "load": 175850.0,
                    "power": 193186,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 40.00000000000006,
                    "load": 263775.0,
                    "power": 249907,
                },
                {
                    "chilled_water_supply_temperature": 12.777777777777828,
                    "condenser_temperature": 40.00000000000006,
                    "load": 351700.0,
                    "power": 306628,
                },
            ],
        }
    ],
    "pumps": [
        {
            "id": "Boiler Pump 1",
            "loop_or_piping": "Boiler Loop 1",
            "speed_control": "FIXED_SPEED",
        },
        {
            "id": "Chiller Pump 1",
            "loop_or_piping": "Chiller Loop 1",
            "speed_control": "FIXED_SPEED",
        },
        {
            "id": "Secondary CHW Pump",
            "loop_or_piping": "Secondary CHW Loop 1",
            "speed_control": "VARIABLE_SPEED",
        },
    ],
    "fluid_loops": [
        {"id": "Boiler Loop 1", "type": "HEATING"},
        {
            "id": "Chiller Loop 1",
            "type": "COOLING",
            "child_loops": [{"id": "Secondary CHW Loop 1", "type": "COOLING"}],
        },
        {"id": "Condenser Loop 1", "type": "CONDENSER"},
    ],
    "heat_rejections": [{"id": "Heat Rejection 1", "loop": "Condenser Loop 1"}],
    "type": "BASELINE_0",
}

TEST_RMD_12 = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_CHILLER = quantify_rmd(TEST_RMD_12)["ruleset_model_descriptions"][0]["chillers"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_12)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_hvac_zone_list_w_area_dict():
    assert is_chiller_performance_app_j(TEST_CHILLER) is True
