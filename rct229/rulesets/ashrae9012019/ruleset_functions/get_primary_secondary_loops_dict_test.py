from rct229.rulesets.ashrae9012019.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMD = {
    "id": "ASHRAE229 1",
    "ruleset_model_descriptions": [
        {
            "id": "RMI 1",
            "buildings": [
                {
                    "id": "Building 1",
                    "building_open_schedule": "Required Building Schedule 1",
                    "building_segments": [
                        {
                            "id": "Building Segment 1",
                            "zones": [
                                {
                                    "id": "Thermal Zone 1",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1",
                                            "is_supply_ducted": True,
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 2",
                                            "is_supply_ducted": True,
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 7",
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chilled Water Loop 1",
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
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "energy_source_type": "NATURAL_GAS",
                }
            ],
            "chillers": [{"id": "Chiller 1", "cooling_loop": "Chiller Loop 1"}],
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
            ],
            "fluid_loops": [
                {"id": "Boiler Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Chilled Water Loop 1", "type": "COOLING"}],
                },
            ],
            "type": "BASELINE_0",
        }
    ],
    "data_timestamp": "2024-02-12T09:00Z",
}


TEST_RMI = quantify_rmr(TEST_RMD)["ruleset_model_descriptions"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_primary_secondary_loops_dict():
    assert get_primary_secondary_loops_dict(TEST_RMI) == {
        "Chiller Loop 1": ["Chilled Water Loop 1"]
    }
