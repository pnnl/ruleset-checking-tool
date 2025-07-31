from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_3 import (
    is_baseline_system_3,
)
from rct229.schema.validate import schema_validate_rpd

SYS_3_TEST_RMD = {
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
                                    "id": "Thermal Zone 3",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 3",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 3",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 3a",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 3a",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 3a",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 3b",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 3b",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 3b",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 3c",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 3c",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 3c",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System Type 3",
                                    "cooling_system": {
                                        "id": "DX Coil 3",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "Furnace Coil 3",
                                        "type": "FURNACE",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 3",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System Type 3a",
                                    "cooling_system": {
                                        "id": "Cooling Coil 3a",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "Furnace Coil 3a",
                                        "type": "FURNACE",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 3a",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 3a"}],
                                    },
                                },
                                {
                                    "id": "System Type 3b",
                                    "cooling_system": {
                                        "id": "DX Coil 3b",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "Heating Coil 3b",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 3b",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 3b"}],
                                    },
                                },
                                {
                                    "id": "System Type 3c",
                                    "cooling_system": {
                                        "id": "Cooling Coil 3c",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "Heating Coil 3c",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 3c",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 3c"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "fluid_loops": [
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


SYS_3_TEST_UNMATCHED_RMD = {
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
                                    "id": "Thermal Zone 3",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 3",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 3c",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System Type Unmatched",
                                    "cooling_system": {
                                        "id": "Cooling Coil",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "Heating Coil",
                                        "type": "OTHER",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 3c"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "fluid_loops": [
                {
                    "id": "Purchased CHW Loop 1",
                    "type": "COOLING",
                },
            ],
            "external_fluid_sources": [
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


def test__TEST_RMD_baseline_system_3__is_valid():
    schema_validation_result = schema_validate_rpd(SYS_3_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_baseline_system_3__is_unmatched_valid():
    schema_validation_result = schema_validate_rpd(SYS_3_TEST_UNMATCHED_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline_system_3__true():
    assert (
        is_baseline_system_3(
            SYS_3_TEST_RMD["ruleset_model_descriptions"][0],
            "System Type 3",
            ["Air Terminal 3"],
            ["Thermal Zone 3"],
        )
        == HVAC_SYS.SYS_3
    )


def test__is_baseline_system_3__test_json_true():
    assert (
        is_baseline_system_3(
            load_system_test_file("System_3_PSZ_AC_Gas_Furnace.json")[
                "ruleset_model_descriptions"
            ][0],
            "System Type 3",
            ["Air Terminal"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_3
    )


def test__is_baseline_system_3A__true():
    assert (
        is_baseline_system_3(
            SYS_3_TEST_RMD["ruleset_model_descriptions"][0],
            "System Type 3a",
            ["Air Terminal 3a"],
            ["Thermal Zone 3a"],
        )
        == HVAC_SYS.SYS_3A
    )


def test__is_baseline_system_3A__test_json_true():
    assert (
        is_baseline_system_3(
            load_system_test_file("System_3a_PSZ_AC_Gas_Furnace.json")[
                "ruleset_model_descriptions"
            ][0],
            "System Type 3",
            ["Air Terminal"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_3A
    )


def test__is_baseline_system_3B__true():
    assert (
        is_baseline_system_3(
            SYS_3_TEST_RMD["ruleset_model_descriptions"][0],
            "System Type 3b",
            ["Air Terminal 3b"],
            ["Thermal Zone 3b"],
        )
        == HVAC_SYS.SYS_3B
    )


def test__is_baseline_system_3B__test_json_true():
    assert (
        is_baseline_system_3(
            load_system_test_file("System_3b_PSZ_AC_Gas_Furnace.json")[
                "ruleset_model_descriptions"
            ][0],
            "System Type 3",
            ["Air Terminal"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_3B
    )


def test__is_baseline_system_3C__true():
    assert (
        is_baseline_system_3(
            SYS_3_TEST_RMD["ruleset_model_descriptions"][0],
            "System Type 3c",
            ["Air Terminal 3c"],
            ["Thermal Zone 3c"],
        )
        == HVAC_SYS.SYS_3C
    )


def test__is_baseline_system_3C_test__json_true():
    assert (
        is_baseline_system_3(
            load_system_test_file("System_3c_PSZ_AC_Gas_Furnace.json")[
                "ruleset_model_descriptions"
            ][0],
            "System Type 3",
            ["Air Terminal"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_3C
    )


def test__is_baseline_system_unmatched__true():
    assert (
        is_baseline_system_3(
            SYS_3_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System Type Unmatched",
            ["Air Terminal 3"],
            ["Thermal Zone 3"],
        )
        == HVAC_SYS.UNMATCHED
    )
