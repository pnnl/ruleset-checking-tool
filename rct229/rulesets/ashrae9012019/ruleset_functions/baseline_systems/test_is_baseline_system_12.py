from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_12 import (
    is_baseline_system_12,
)
from rct229.schema.validate import schema_validate_rpd

SYS_12_TEST_RMD = {
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
                                            "id": "CAV Air Terminal 1",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 12",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "CAV Air Terminal 2",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 12a",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 3",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "CAV Air Terminal 3",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 12b",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 4",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "CAV Air Terminal 4",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 12d",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 12",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "Boiler Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 12a",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chilled Water Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "Boiler Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 12b",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 12c",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chilled Water Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
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
                    "loop": "Chilled Water Loop 1",
                    "type": "CHILLED_WATER",
                },
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
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
                {
                    "id": "CHW Pump 1",
                    "loop_or_piping": "Chilled Water Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "HW Pump 1",
                    "loop_or_piping": "Purchased HW Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
            ],
            "fluid_loops": [
                {"id": "Boiler Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary CHW Loop 1", "type": "COOLING"}],
                },
                {"id": "Chilled Water Loop 1", "type": "COOLING"},
                {"id": "Purchased HW Loop 1", "type": "HEATING"},
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

SYS_12_TEST_UNMATCHED_RMD = {
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
                                    "id": "Thermal Zone 12",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 12",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type Unmatched",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System Type Unmatched",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
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
                    "loop": "Chilled Water Loop 1",
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
                {
                    "id": "CHW Pump 1",
                    "loop_or_piping": "Chilled Water Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "HW Pump 1",
                    "loop_or_piping": "HW Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
            ],
            "fluid_loops": [
                {"id": "Boiler Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary CHW Loop 1", "type": "COOLING"}],
                },
                {"id": "Chilled Water Loop 1", "type": "COOLING"},
                {"id": "HW Loop 1", "type": "HEATING"},
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


def test__TEST_RMD_baseline_system_12__is_valid():
    schema_validation_result = schema_validate_rpd(SYS_12_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_baseline_system_12__is_unmatched_valid():
    schema_validation_result = schema_validate_rpd(SYS_12_TEST_UNMATCHED_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline_system_12__true():
    assert (
        is_baseline_system_12(
            SYS_12_TEST_RMD["ruleset_model_descriptions"][0],
            "System 12",
            ["CAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_12
    )


def test__is_baseline_system_12__test_json_true():
    assert (
        is_baseline_system_12(
            load_system_test_file("System 12_CAV_SZ_HW.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 12",
            ["CAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_12
    )


def test__is_baseline_system_12A__true():
    assert (
        is_baseline_system_12(
            SYS_12_TEST_RMD["ruleset_model_descriptions"][0],
            "System 12a",
            ["CAV Air Terminal 2"],
            ["Thermal Zone 2"],
        )
        == HVAC_SYS.SYS_12A
    )


def test__is_baseline_system_12A__test_json_true():
    assert (
        is_baseline_system_12(
            load_system_test_file("System 12a_CAV_SZ_HW.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 12",
            ["CAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_12A
    )


def test__is_baseline_system_12B__true():
    assert (
        is_baseline_system_12(
            SYS_12_TEST_RMD["ruleset_model_descriptions"][0],
            "System 12b",
            ["CAV Air Terminal 3"],
            ["Thermal Zone 3"],
        )
        == HVAC_SYS.SYS_12B
    )


def test__is_baseline_system_12B__test_json_true():
    assert (
        is_baseline_system_12(
            load_system_test_file("System 12b_CAV_SZ_HW.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 12",
            ["CAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_12B
    )


def test__is_baseline_system_unmatched__true():
    assert (
        is_baseline_system_12(
            SYS_12_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched",
            ["Air Terminal 12"],
            ["Thermal Zone 12"],
        )
        == HVAC_SYS.UNMATCHED
    )
