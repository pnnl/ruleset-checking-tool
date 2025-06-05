from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_8 import (
    is_baseline_system_8,
)
from rct229.schema.validate import schema_validate_rpd

SYS_8_TEST_RMD = {
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
                                    "id": "Thermal Zone 8",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8",
                                            "heating_source": "ELECTRIC",
                                            "heating_from_loop": "Boiler Loop 1",
                                            "fan": {"id": "fan 8"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 8a",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8a",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8a",
                                            "heating_source": "ELECTRIC",
                                            "heating_from_loop": "Boiler Loop 1",
                                            "fan": {"id": "fan 8a"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 8b",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8b",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8b",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "fan": {"id": "fan 8b"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 8c",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8c",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8c",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "fan": {"id": "fan 8c"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 8",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "type": "ELECTRIC_RESISTANCE",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 8a",
                                    "cooling_system": {
                                        "id": "CHW Coil 8a",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased Chilled Water Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8a",
                                        "type": "ELECTRIC_RESISTANCE",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8a",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 8a"}],
                                        "return_fans": [{"id": "Return Fan 8a"}],
                                    },
                                },
                                {
                                    "id": "System 8b",
                                    "cooling_system": {
                                        "id": "CHW Coil 8b",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8b",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8b",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 8c",
                                    "cooling_system": {
                                        "id": "CHW Coil 8C",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased Chilled Water Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8C",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8C",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
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
                    "energy_source_type": "NATURAL_GAS",
                }
            ],
            "external_fluid_sources": [
                {
                    "id": "Purchased CW 1",
                    "loop": "Purchased Chilled Water Loop 1",
                    "type": "CHILLED_WATER",
                },
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                },
                {
                    "id": "Purchased CW 2",
                    "loop": "Chilled Water Loop 2",
                    "type": "CHILLED_WATER",
                },
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
                {
                    "id": "Secondary CHW Pump",
                    "loop_or_piping": "Secondary CHW Loop 1",
                    "speed_control": "VARIABLE_SPEED",
                },
            ],
            "fluid_loops": [
                {"id": "Boiler Loop 1", "type": "HEATING"},
                {"id": "Purchased HW Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary CHW Loop 1", "type": "COOLING"}],
                },
                {"id": "Purchased Chilled Water Loop 1", "type": "COOLING"},
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

SYS_8_TEST_UNMATCHED_RMD = {
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
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type Unmatched 1",
                                            "heating_source": "ELECTRIC",
                                            "heating_from_loop": "Boiler Loop 1",
                                            "fan": {"id": "fan 1"},
                                            "fan_configuration": "PARALLEL",
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
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type Unmatched",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "fan": {"id": "fan 2"},
                                            "fan_configuration": "PARALLEL",
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
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type Unmatched 3",
                                            "heating_source": "ELECTRIC",
                                            # "heating_from_loop": "Purchased HW Loop 1",
                                            "fan": {"id": "fan 3"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 4",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 4",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type Unmatched 4",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "fan": {"id": "fan 4"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System Type Unmatched 1",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chilled Water Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "type": "ELECTRIC_RESISTANCE",
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
                                    "cooling_system": {
                                        "id": "CHW Coil 8b",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8b",
                                        "type": "OTHER",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8b",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System Type Unmatched 3",
                                    "cooling_system": {
                                        "id": "CHW Coil 8b",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 3",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 3",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System Type Unmatched 4",
                                    "cooling_system": {
                                        "id": "CHW Coil 4",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chilled Water Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 4",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 4",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
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
                    "energy_source_type": "NATURAL_GAS",
                }
            ],
            "external_fluid_sources": [
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                },
                {
                    "id": "Purchased CW 2",
                    "loop": "Chilled Water Loop 2",
                    "type": "CHILLED_WATER",
                },
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
                {
                    "id": "Secondary CHW Pump",
                    "loop_or_piping": "Secondary CHW Loop 1",
                    "speed_control": "VARIABLE_SPEED",
                },
            ],
            "fluid_loops": [
                {"id": "Boiler Loop 1", "type": "HEATING"},
                {"id": "Purchased HW Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary CHW Loop 1", "type": "COOLING"}],
                },
                {"id": "Chilled Water Loop 1", "type": "COOLING"},
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


def test__TEST_RMD_baseline_system_8__is_valid():
    schema_validation_result = schema_validate_rpd(SYS_8_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_baseline_system_8__is_unmatched_valid():
    schema_validation_result = schema_validate_rpd(SYS_8_TEST_UNMATCHED_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline_system_8__true():
    assert (
        is_baseline_system_8(
            SYS_8_TEST_RMD["ruleset_model_descriptions"][0],
            "System 8",
            ["VAV Air Terminal 8"],
            ["Thermal Zone 8"],
        )
        == HVAC_SYS.SYS_8
    )


def test__is_baseline_system_8__test_json_true():
    assert (
        is_baseline_system_8(
            load_system_test_file("System_8_PFP_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 8",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_8
    )


def test__is_baseline_system_8A__true():
    assert (
        is_baseline_system_8(
            SYS_8_TEST_RMD["ruleset_model_descriptions"][0],
            "System 8a",
            ["VAV Air Terminal 8a"],
            ["Thermal Zone 8a"],
        )
        == HVAC_SYS.SYS_8A
    )


def test__is_baseline_system_8A__test_json_true():
    assert (
        is_baseline_system_8(
            load_system_test_file("System_8a_PFP_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 8",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_8A
    )


def test__is_baseline_system_8B__true():
    assert (
        is_baseline_system_8(
            SYS_8_TEST_RMD["ruleset_model_descriptions"][0],
            "System 8b",
            ["VAV Air Terminal 8b"],
            ["Thermal Zone 8b"],
        )
        == HVAC_SYS.SYS_8B
    )


def test__is_baseline_system_8B__test_json_true():
    assert (
        is_baseline_system_8(
            load_system_test_file("System_8b_PFP_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 8",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_8B
    )


def test__is_baseline_system_8C__true():
    assert (
        is_baseline_system_8(
            SYS_8_TEST_RMD["ruleset_model_descriptions"][0],
            "System 8c",
            ["VAV Air Terminal 8c"],
            ["Thermal Zone 8c"],
        )
        == HVAC_SYS.SYS_8C
    )


def test__is_baseline_system_8C__test_json_true():
    assert (
        is_baseline_system_8(
            load_system_test_file("System_8c_PFP_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 8",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_8C
    )


def test__is_baseline_system_unmatched1__true():
    assert (
        is_baseline_system_8(
            SYS_8_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched 1",
            ["Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.UNMATCHED
    )


def test__is_baseline_system_unmatched2__true():
    assert (
        is_baseline_system_8(
            SYS_8_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched 2",
            ["Air Terminal 2"],
            ["Thermal Zone 2"],
        )
        == HVAC_SYS.UNMATCHED
    )


def test__is_baseline_system_unmatched3__true():
    assert (
        is_baseline_system_8(
            SYS_8_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched 3",
            ["Air Terminal 3"],
            ["Thermal Zone 3"],
        )
        == HVAC_SYS.UNMATCHED
    )


def test__is_baseline_system_unmatched4__true():
    assert (
        is_baseline_system_8(
            SYS_8_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched 4",
            ["Air Terminal 4"],
            ["Thermal Zone 4"],
        )
        == HVAC_SYS.UNMATCHED
    )
