from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_11_1 import (
    is_baseline_system_11_1,
)
from rct229.schema.validate import schema_validate_rpd

SYS_11_1_TEST_RMD = {
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
                                    "id": "Thermal Zone 1B",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1B",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 11B",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 11",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1A",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1A",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 11A",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1C",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1C",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 11C",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System Type 11B",
                                    "cooling_system": {
                                        "id": "CHW Coil 1B",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1B",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1B",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1B"}],
                                        "return_fans": [{"id": "Return Fan 1B"}],
                                    },
                                },
                                {
                                    "id": "System Type 11",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1",
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
                                    "id": "System Type 11A",
                                    "cooling_system": {
                                        "id": "CHW Coil 1A",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1A",
                                        "type": "ELECTRIC_RESISTANCE",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1A",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1A"}],
                                        "return_fans": [{"id": "Return Fan 1A"}],
                                    },
                                },
                                {
                                    "id": "System Type 11C",
                                    "cooling_system": {
                                        "id": "CHW Coil 1C",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1C",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1C",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1C"}],
                                        "return_fans": [{"id": "Return Fan 1C"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "chillers": [
                {
                    "id": "Chiller 1",
                    "cooling_loop": "Chiller Loop 1",
                    "energy_source_type": "ELECTRICITY",
                }
            ],
            "external_fluid_sources": [
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                },
                {
                    "id": "Purchased CHW",
                    "loop": "Purchased CHW Loop 1",
                    "type": "CHILLED_WATER",
                },
            ],
            "pumps": [
                {
                    "id": "HW Pump 1",
                    "loop_or_piping": "Purchased HW Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "Chiller Pump 1",
                    "loop_or_piping": "Chiller Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
            ],
            "fluid_loops": [
                {"id": "Purchased HW Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary Loop 1", "type": "COOLING"}],
                },
                {
                    "id": "Purchased CHW Loop 1",
                    "type": "COOLING",
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

SYS_11_1_TEST_UNMATCHED_RMD = {
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
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 11A",
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
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 11C",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System Type Unmatched 1",
                                    "cooling_system": {
                                        "id": "CHW Coil 1A",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1A",
                                        "type": "ELECTRIC_RESISTANCE",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1A",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1A"}],
                                        "return_fans": [{"id": "Return Fan 1A"}],
                                    },
                                },
                                {
                                    "id": "System Type Unmatched 2",
                                    "cooling_system": {
                                        "id": "CHW Coil 1C",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1C",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1C",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1C"}],
                                        "return_fans": [{"id": "Return Fan 1C"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "chillers": [
                {
                    "id": "Chiller 1",
                    "cooling_loop": "Chiller Loop 1",
                    "energy_source_type": "ELECTRICITY",
                }
            ],
            "external_fluid_sources": [
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                },
            ],
            "pumps": [
                {
                    "id": "HW Pump 1",
                    "loop_or_piping": "Purchased HW Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "Chiller Pump 1",
                    "loop_or_piping": "Chiller Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
            ],
            "fluid_loops": [
                {"id": "Purchased HW Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary Loop 1", "type": "COOLING"}],
                },
                {
                    "id": "CHW Loop 1",
                    "type": "COOLING",
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


def test__TEST_RMD_baseline_system_11_1__is_valid():
    schema_validation_result = schema_validate_rpd(SYS_11_1_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_baseline_system_11_1__is_unmatched_valid():
    schema_validation_result = schema_validate_rpd(SYS_11_1_TEST_UNMATCHED_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline__system_11_1__true():
    assert (
        is_baseline_system_11_1(
            SYS_11_1_TEST_RMD["ruleset_model_descriptions"][0],
            "System Type 11",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_11_1
    )


def test__is_baseline_system_11_1__test_json_true():
    assert (
        is_baseline_system_11_1(
            load_system_test_file("System_11.1_VAV_SZ.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 11",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_11_1
    )


def test__is_baseline_system_11_1A__true():
    assert (
        is_baseline_system_11_1(
            SYS_11_1_TEST_RMD["ruleset_model_descriptions"][0],
            "System Type 11A",
            ["VAV Air Terminal 1A"],
            ["Thermal Zone 1A"],
        )
        == HVAC_SYS.SYS_11_1A
    )


def test__is_baseline_system_11_1A__test_json_true():
    assert (
        is_baseline_system_11_1(
            load_system_test_file("System_11.1a_VAV_SZ.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 11",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_11_1A
    )


def test__is_baseline_system_11_1B__true():
    assert (
        is_baseline_system_11_1(
            SYS_11_1_TEST_RMD["ruleset_model_descriptions"][0],
            "System Type 11B",
            ["VAV Air Terminal 1B"],
            ["Thermal Zone 1B"],
        )
        == HVAC_SYS.SYS_11_1B
    )


def test__is_baseline_system_11_1B__test_json_true():
    assert (
        is_baseline_system_11_1(
            load_system_test_file("System_11.1b_VAV_SZ.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 11",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_11_1B
    )


def test__is_baseline_system_11_1C__true():
    assert (
        is_baseline_system_11_1(
            SYS_11_1_TEST_RMD["ruleset_model_descriptions"][0],
            "System Type 11C",
            ["VAV Air Terminal 1C"],
            ["Thermal Zone 1C"],
        )
        == HVAC_SYS.SYS_11_1C
    )


def test__is_baseline_system_11_1C__test_json_true():
    assert (
        is_baseline_system_11_1(
            load_system_test_file("System_11.1c_VAV_SZ.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 11",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_11_1C
    )


def test__is_baseline_system_11_1__no_ays_true():
    # `no_sys` means there is no matched system and this is for testing when there is no matching system (11.1, 11.1A, 11.1B, 11.1C)
    assert (
        is_baseline_system_11_1(
            SYS_11_1_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched 1",
            ["Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.UNMATCHED
    )


def test__is_baseline_system_11_1__no_ays_true():
    # `no_sys` means there is no matched system and this is for testing when there is no matching system (11.1, 11.1A, 11.1B, 11.1C)
    assert (
        is_baseline_system_11_1(
            SYS_11_1_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched 2",
            ["Air Terminal 2"],
            ["Thermal Zone 2"],
        )
        == HVAC_SYS.UNMATCHED
    )
