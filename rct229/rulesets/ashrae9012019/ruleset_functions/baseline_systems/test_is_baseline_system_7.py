from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_7 import (
    is_baseline_system_7,
)
from rct229.schema.validate import schema_validate_rpd

SYS_7_TEST_RMD = {
    "id": "ASHRAE229 1",
    "ruleset_model_descriptions": [
        {
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
                                            "id": "VAV Air Terminal 1",
                                            "is_supply_ducted": True,
                                            "heating_from_loop": "Boiler Loop 1",
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
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
                                            "heating_from_loop": "Boiler Loop 1",
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7a",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 3",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 3",
                                            "is_supply_ducted": True,
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7b",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 4",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 4",
                                            "is_supply_ducted": True,
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7c",
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
                                        "id": "Cooling Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 7a",
                                    "preheat_system": {
                                        "id": "Preheat Coil 2",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "cooling_system": {
                                        "id": "Cooling Coil 2",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 2",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 2"}],
                                        "return_fans": [{"id": "Return Fan 2"}],
                                    },
                                },
                                {
                                    "id": "System 7b",
                                    "preheat_system": {
                                        "id": "Preheat Coil 3",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "cooling_system": {
                                        "id": "Cooling Coil 3",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 3",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 3"}],
                                        "return_fans": [{"id": "Return Fan 3"}],
                                    },
                                },
                                {
                                    "id": "System 7c",
                                    "preheat_system": {
                                        "id": "Preheat Coil 4",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "cooling_system": {
                                        "id": "Cooling Coil 4",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 4",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 4"}],
                                        "return_fans": [{"id": "Return Fan 4"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "boilers": [
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "design_capacity": 117228.44444444445,
                }
            ],
            "chillers": [
                {
                    "id": "Chiller 1",
                    "cooling_loop": "Chiller Loop 1",
                    "condensing_loop": "Condenser Loop 1",
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
            ],
            "fluid_loops": [
                {
                    "id": "Boiler Loop 1",
                    "type": "HEATING",
                    "heating_design_and_control": {
                        "id": "DAC1",
                        "minimum_flow_fraction": 0.25,
                    },
                },
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary Loop 1", "type": "COOLING"}],
                },
                {
                    "id": "Purchased HW Loop 1",
                    "type": "HEATING",
                },
                {
                    "id": "Purchased CHW Loop 1",
                    "type": "COOLING",
                },
            ],
            "external_fluid_sources": [
                {
                    "id": "Purchased HW",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                },
                {
                    "id": "Purchased CHW",
                    "loop": "Purchased CHW Loop 1",
                    "type": "CHILLED_WATER",
                },
            ],
            "type": "BASELINE_0",
        }
    ],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

SYS_7_TEST_UNMATCHED_RMD = {
    "id": "ASHRAE229 1",
    "ruleset_model_descriptions": [
        {
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
                                            "id": "Air Terminal 1",
                                            "is_supply_ducted": True,
                                            "heating_from_loop": "Boiler Loop 1",
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7a",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 2",
                                            "is_supply_ducted": True,
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type Unmatched 2",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 3",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 3",
                                            "is_supply_ducted": True,
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type Unmatched 3",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System Type Unmatched 1",
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "cooling_system": {
                                        "id": "Cooling Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "CHW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System Type Unmatched 2",
                                    "preheat_system": {
                                        "id": "Preheat Coil 3",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "HW Loop 1",
                                    },
                                    "cooling_system": {
                                        "id": "Cooling Coil 3",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 2",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 2"}],
                                        "return_fans": [{"id": "Return Fan 2"}],
                                    },
                                },
                                {
                                    "id": "System Type Unmatched 3",
                                    "preheat_system": {
                                        "id": "Preheat Coil 3",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "cooling_system": {
                                        "id": "Cooling Coil 4",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "CHW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 3",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 3"}],
                                        "return_fans": [{"id": "Return Fan 3"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "boilers": [
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "design_capacity": 117228.44444444445,
                }
            ],
            "chillers": [
                {
                    "id": "Chiller 1",
                    "cooling_loop": "Chiller Loop 1",
                    "condensing_loop": "Condenser Loop 1",
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
            ],
            "fluid_loops": [
                {
                    "id": "Boiler Loop 1",
                    "type": "HEATING",
                    "heating_design_and_control": {
                        "id": "DAC1",
                        "minimum_flow_fraction": 0.25,
                    },
                },
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary Loop 1", "type": "COOLING"}],
                },
                {
                    "id": "HW Loop 1",
                    "type": "HEATING",
                },
                {
                    "id": "Purchased HW Loop 1",
                    "type": "HEATING",
                },
                {
                    "id": "CHW Loop 1",
                    "type": "COOLING",
                },
            ],
            "external_fluid_sources": [
                {
                    "id": "Purchased HW",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                },
                {
                    "id": "Purchased CHW",
                    "loop": "Purchased CHW Loop 1",
                    "type": "CHILLED_WATER",
                },
            ],
            "type": "BASELINE_0",
        }
    ],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}


def test__TEST_RMD_baseline_system_7__is_valid():
    schema_validation_result = schema_validate_rpd(SYS_7_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_baseline_system_7__is_unmatched_valid():
    schema_validation_result = schema_validate_rpd(SYS_7_TEST_UNMATCHED_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline_system_7__true():
    assert (
        is_baseline_system_7(
            SYS_7_TEST_RMD["ruleset_model_descriptions"][0],
            "System 7",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_7
    )


def test__is_baseline_system_7__test_json_true():
    assert (
        is_baseline_system_7(
            load_system_test_file("System_7_VAV_HW_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 7",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_7
    )


def test__is_baseline_system_7A__true():
    assert (
        is_baseline_system_7(
            SYS_7_TEST_RMD["ruleset_model_descriptions"][0],
            "System 7a",
            ["VAV Air Terminal 2"],
            ["Thermal Zone 2"],
        )
        == HVAC_SYS.SYS_7A
    )


def test__is_baseline_system_7A__test_json_true():
    assert (
        is_baseline_system_7(
            load_system_test_file("System_7a_VAV_HW_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 7",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_7A
    )


def test__is_baseline_system_7B__true():
    assert (
        is_baseline_system_7(
            SYS_7_TEST_RMD["ruleset_model_descriptions"][0],
            "System 7b",
            ["VAV Air Terminal 3"],
            ["Thermal Zone 3"],
        )
        == HVAC_SYS.SYS_7B
    )


def test__is_baseline_system_7B__test_json_true():
    assert (
        is_baseline_system_7(
            load_system_test_file("System_7b_VAV_HW_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 7",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_7B
    )


def test__is_baseline_system_7C_true():
    assert (
        is_baseline_system_7(
            SYS_7_TEST_RMD["ruleset_model_descriptions"][0],
            "System 7c",
            ["VAV Air Terminal 4"],
            ["Thermal Zone 4"],
        )
        == HVAC_SYS.SYS_7C
    )


def test__is_baseline_system_7C__test_json_true():
    assert (
        is_baseline_system_7(
            load_system_test_file("System_7c_VAV_HW_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 7",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_7C
    )


def test__is_baseline_system_unmatched1__true():
    assert (
        is_baseline_system_7(
            SYS_7_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched 1",
            ["Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.UNMATCHED
    )


def test__is_baseline_system_unmatched2__true():
    assert (
        is_baseline_system_7(
            SYS_7_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched 2",
            ["Air Terminal 2"],
            ["Thermal Zone 2"],
        )
        == HVAC_SYS.UNMATCHED
    )


def test__is_baseline_system_unmatched3__true():
    assert (
        is_baseline_system_7(
            SYS_7_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched 3",
            ["Air Terminal 3"],
            ["Thermal Zone 3"],
        )
        == HVAC_SYS.UNMATCHED
    )
