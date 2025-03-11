from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_6 import (
    is_baseline_system_6,
)
from rct229.schema.validate import schema_validate_rpd

SYS_6_TEST_RMD = {
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
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 6",
                                            "heating_source": "ELECTRIC",
                                            "fan": {
                                                "id": "Terminal Fan 1",
                                            },
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
                                            "id": "VAV Air Terminal 2",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 6B",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "fan": {
                                                "id": "Terminal Fan 2",
                                            },
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 6",
                                    "cooling_system": {
                                        "id": "DX Coil 1",
                                        "type": "DIRECT_EXPANSION",
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
                                    "id": "System 6B",
                                    "cooling_system": {
                                        "id": "DX Coil 2",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 2",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 2",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 2"}],
                                        "return_fans": [{"id": "Return Fan 2"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "external_fluid_sources": [
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                }
            ],
            "pumps": [
                {
                    "id": "HW Pump 1",
                    "loop_or_piping": "Purchased HW Loop 1",
                    "speed_control": "FIXED_SPEED",
                }
            ],
            "fluid_loops": [{"id": "Purchased HW Loop 1", "type": "HEATING"}],
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

SYS_6_TEST_UNMATCHED_RMD = {
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
                                            "id": "VAV Air Terminal 3",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 6 Unmatched",
                                            "heating_source": "HOT_WATER",
                                            "fan": {
                                                "id": "Terminal Fan 3",
                                            },
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 6 Unmatched",
                                    "cooling_system": {
                                        "id": "DX Coil 2",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 3",
                                        "type": "OTHER",
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


def test__TEST_RMD_baseline_system_6__is_valid():
    schema_validation_result = schema_validate_rpd(SYS_6_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_baseline_system_6__is_unmatched_valid():
    schema_validation_result = schema_validate_rpd(SYS_6_TEST_UNMATCHED_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline_system_6__true():
    assert (
        is_baseline_system_6(
            SYS_6_TEST_RMD["ruleset_model_descriptions"][0],
            "System 6",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_6
    )


def test__is_baseline_system_6_test_json__true():
    assert (
        is_baseline_system_6(
            load_system_test_file("System_6_PVAV_Elec_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 6",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_6
    )


def test__is_baseline_system_6B__true():
    assert (
        is_baseline_system_6(
            SYS_6_TEST_RMD["ruleset_model_descriptions"][0],
            "System 6B",
            ["VAV Air Terminal 2"],
            ["Thermal Zone 2"],
        )
        == HVAC_SYS.SYS_6B
    )


def test_is_baseline_system_6B__test_json_true():
    assert (
        is_baseline_system_6(
            load_system_test_file("System_6b_PVAV_Elec_Reheat.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 6",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_6B
    )


def test__is_baseline_system_unmatched__true():
    assert (
        is_baseline_system_6(
            SYS_6_TEST_UNMATCHED_RMD["ruleset_model_descriptions"][0],
            "System 6 Unmatched",
            ["VAV Air Terminal 3"],
            ["Thermal Zone 3"],
        )
        == HVAC_SYS.UNMATCHED
    )
