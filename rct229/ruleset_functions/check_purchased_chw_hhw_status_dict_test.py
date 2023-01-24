from rct229.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)
from rct229.schema.validate import schema_validate_rmr

TEST_BUILDING_HEATING_SYS = {
    "id": "RMD 1",
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
                                    "id": "CAV Air Terminal 1",
                                    "is_supply_ducted": True,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "Testing system",
                                    "heating_from_loop": "Boiler Loop 1",
                                }
                            ],
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "Testing system",
                            "cooling_system": {
                                "id": "CHW Coil 1",
                                "cooling_system_type": "FLUID_LOOP",
                                "chilled_water_loop": "Chilled Water Loop 1",
                            },
                            "heating_system": {
                                "id": "Boiler Coil 1",
                                "heating_system_type": "FLUID_LOOP",
                                "hot_water_loop": "Boiler Loop 1",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 1",
                                "fan_control": "CONSTANT",
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
            "loop": "Boiler HW 1",
            "energy_source_type": "NATURAL_GAS",
        }
    ],
    "external_fluid_source": [
        {
            "id": "Chilled Water 1",
            "loop": "Chilled Water Loop 1",
            "type": "CHILLED_WATER",
        },
        {
            "id": "Boiler 1",
            "loop": "Boiler Loop 1",
            "type": "HOT_WATER",
        },
    ],
    "pumps": [
        {
            "id": "Boiler Pump 1",
            "loop_or_piping": "Boiler Loop 1",
            "speed_control": "FIXED_SPEED",
        },
        {
            "id": "CHW Pump 1",
            "loop_or_piping": "Chilled Water Loop 1",
            "speed_control": "FIXED_SPEED",
        },
    ],
    "fluid_loops": [
        {
            "id": "Chilled Water Loop 1",
            "type": "COOLING",
            "child_loops": [{"id": "CHW1 Child Loop 1"}],
        },
        {
            "id": "Boiler Loop 1",
            "type": "HEATING",
            "child_loops": [{"id": "HW1 Child Loop 1"}],
        },
    ],
}

TEST_BUILDING_PREHEAT_SYS = {
    "id": "RMD 1",
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
                                    "id": "CAV Air Terminal 1",
                                    "is_supply_ducted": True,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "Testing system",
                                    "cooling_from_loop": "Chilled Water Loop 1",
                                }
                            ],
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "Testing system",
                            "cooling_system": {
                                "id": "CHW Coil 1",
                                "cooling_system_type": "FLUID_LOOP",
                                "chilled_water_loop": "Chilled Water Loop 1",
                            },
                            "preheat_system": {
                                "id": "Preheat Coil 1",
                                "heating_system_type": "FLUID_LOOP",
                                "hot_water_loop": "Preheat Loop 1",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 1",
                                "fan_control": "CONSTANT",
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
            "loop": "Boiler HW 1",
            "energy_source_type": "NATURAL_GAS",
        }
    ],
    "external_fluid_source": [
        {
            "id": "Chilled Water 1",
            "loop": "Chilled Water Loop 1",
            "type": "CHILLED_WATER",
        },
        {
            "id": "Preheat 1",
            "loop": "Preheat Loop 1",
            "type": "HOT_WATER",
        },
    ],
    "pumps": [
        {
            "id": "Preheat Pump 1",
            "loop_or_piping": "Preheat Loop 1",
            "speed_control": "FIXED_SPEED",
        },
        {
            "id": "CHW Pump 1",
            "loop_or_piping": "Chilled Water Loop 1",
            "speed_control": "FIXED_SPEED",
        },
    ],
    "fluid_loops": [
        {
            "id": "Chilled Water Loop 1",
            "type": "COOLING",
            "child_loops": [{"id": "CHW1 Child Loop 1"}],
        },
        {
            "id": "Preheat Loop 1",
            "type": "HEATING",
            "child_loops": [{"id": "HW1 Child Loop 1"}],
        },
    ],
}

TEST_BUILDING_FALSE = {
    "id": "RMD 1",
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
                                    "id": "CAV Air Terminal 1",
                                    "is_supply_ducted": True,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 12",
                                }
                            ],
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 12",
                            "cooling_system": {
                                "id": "CHW Coil 1",
                                "cooling_system_type": "FLUID_LOOP",
                                "chilled_water_loop": "Chilled Water Loop 1",
                            },
                            "heating_system": {
                                "id": "Boiler Coil 1",
                                "heating_system_type": "FLUID_LOOP",
                                "hot_water_loop": "Boiler Loop 1",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 1",
                                "fan_control": "CONSTANT",
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
            "loop": "Boiler HW 1",
            "energy_source_type": "NATURAL_GAS",
        }
    ],
    "pumps": [
        {
            "id": "Boiler Pump 1",
            "loop_or_piping": "Boiler Loop 1",
            "speed_control": "FIXED_SPEED",
        },
        {
            "id": "CHW Pump 1",
            "loop_or_piping": "Chilled Water Loop 1",
            "speed_control": "FIXED_SPEED",
        },
    ],
    "fluid_loops": [
        {
            "id": "Chilled Water Loop 1",
            "type": "COOLING",
            "child_loops": [{"id": "CHW1 Child Loop 1"}],
        },
        {
            "id": "Boiler Loop 1",
            "type": "HEATING",
            "child_loops": [{"id": "HW1 Child Loop 1"}],
        },
    ],
}


TEST_RMD_TRUE = {
    "id": "ASHRAE229",
    "ruleset_model_instances": [TEST_BUILDING_HEATING_SYS],
}
TEST_RMD_FALSE = {"id": "ASHRAE229", "ruleset_model_instances": [TEST_BUILDING_FALSE]}


def test__TEST_RMD_TRUE__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_TRUE)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_FALSE__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FALSE)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_check_purchased_chw_hhw_true():
    assert check_purchased_chw_hhw_status_dict(TEST_BUILDING_HEATING_SYS) == {
        "purchased_cooling": True,
        "purchased_heating": True,
    }


def test_check_purchased_chw_hhw_true2():
    assert check_purchased_chw_hhw_status_dict(TEST_BUILDING_PREHEAT_SYS) == {
        "purchased_cooling": True,
        "purchased_heating": True,
    }


def test_check_purchased_chw_hhw_false():
    assert check_purchased_chw_hhw_status_dict(TEST_BUILDING_FALSE) == {
        "purchased_cooling": False,
        "purchased_heating": False,
    }
