from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_hvac_sys_fan_objs_autosized import (
    are_all_hvac_sys_fan_objs_autosized,
)
from rct229.schema.validate import schema_validate_rmr

TEST_RMD_TRUE = {
    "id": "test_rmd",
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
                                    "id": "Air Terminal",
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 3",
                                    "fan": {
                                        "id": "Terminal fan 1",
                                        "is_airflow_autosized": True,
                                    },
                                }
                            ],
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 3",
                            "heating_system": {
                                "id": "Furnace Coil 1",
                                "heating_system_type": "FURNACE",
                                "energy_source_type": "NATURAL_GAS",
                            },
                        },
                    ],
                }
            ],
        }
    ],
}

TEST_RMD_FAN_SYSTEM = {
    "id": "test_rmd",
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
                                    "id": "Air Terminal",
                                    "type": "CONSTANT_AIR_VOLUME",
                                }
                            ],
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 1",
                            "heating_system": {
                                "id": "Furnace Coil 1",
                                "heating_system_type": "FURNACE",
                                "energy_source_type": "NATURAL_GAS",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 1",
                                "fan_control": "CONSTANT",
                                "supply_fans": [
                                    {"id": "Supply Fan 1", "is_airflow_autosized": True}
                                ],
                            },
                        },
                        {
                            "id": "System 2",
                            "heating_system": {
                                "id": "Furnace Coil 1",
                                "heating_system_type": "FURNACE",
                                "energy_source_type": "NATURAL_GAS",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 1",
                                "fan_control": "CONSTANT",
                                "supply_fans": [
                                    {
                                        "id": "Supply Fan 1",
                                        "is_airflow_autosized": False,
                                    }
                                ],
                            },
                        },
                    ],
                }
            ],
        }
    ],
}


TEST_RMD_TERMINAL = {
    "id": "test_rmd",
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
                                    "id": "Air Terminal 1",
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                    "fan": {
                                        "id": "Terminal fan 1",
                                        "is_airflow_autosized": True,
                                    },
                                },
                                {
                                    "id": "Air Terminal 2",
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                    "fan": {
                                        "id": "Terminal fan 2",
                                        "is_airflow_autosized": False,
                                    },
                                },
                            ],
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 1",
                            "heating_system": {
                                "id": "Furnace Coil 1",
                                "heating_system_type": "FURNACE",
                                "energy_source_type": "NATURAL_GAS",
                            },
                        },
                        {
                            "id": "System 2",
                            "heating_system": {
                                "id": "Furnace Coil 1",
                                "heating_system_type": "FURNACE",
                                "energy_source_type": "NATURAL_GAS",
                            },
                        },
                    ],
                }
            ],
        }
    ],
}


TEST_RMD_TRUE = {"id": "229_01", "ruleset_model_instances": [TEST_RMD_TRUE]}

TEST_RMD_FULL_FAN_SYSTEM = {
    "id": "229_01",
    "ruleset_model_instances": [TEST_RMD_FAN_SYSTEM],
}

TEST_RMD_FULL_TERMINAL = {
    "id": "229_01",
    "ruleset_model_instances": [TEST_RMD_TERMINAL],
}


def test__TEST_RMD_TRUE__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_TRUE)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_FAN_SYSTEM__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL_FAN_SYSTEM)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_TERMINAL__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL_TERMINAL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__are_all_hvac_sys_fan_objs_autosized__true():
    assert are_all_hvac_sys_fan_objs_autosized(TEST_RMD_TRUE) == True


def test__are_all_hvac_sys_fan_objs_autosized_fan__system_false():
    assert are_all_hvac_sys_fan_objs_autosized(TEST_RMD_FAN_SYSTEM) == False


def test__are_all_hvac_sys_fan_objs_autosized__terminal_false():
    assert are_all_hvac_sys_fan_objs_autosized(TEST_RMD_TERMINAL) == False
