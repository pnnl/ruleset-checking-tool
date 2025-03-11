from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_9 import (
    is_baseline_system_9,
)
from rct229.schema.validate import schema_validate_rpd

SYS_9_TEST_RMD = {
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
                                    "id": "Thermal Zone 9",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Constant Air Terminal 9",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 9",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 9",
                                    "heating_system": {
                                        "id": "Furnace Coil 1",
                                        "type": "FURNACE",
                                        "energy_source_type": "NATURAL_GAS",
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

SYS_9B_TEST_RMD = {
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
                                    "id": "Thermal Zone 9B",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Constant Air Terminal 9B",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "heating_source": "HOT_WATER",
                                            "fan": {"id": "fan 1"},
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 9B",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 9B",
                                }
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


def test__TEST_RMD_baseline_system_9__is_valid():
    schema_validation_result = schema_validate_rpd(SYS_9_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_baseline_system_9B__is_valid():
    schema_validation_result = schema_validate_rpd(SYS_9B_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline_system_9__true():
    assert (
        is_baseline_system_9(
            SYS_9_TEST_RMD["ruleset_model_descriptions"][0],
            "System 9",
            ["Constant Air Terminal 9"],
            ["Thermal Zone 9"],
        )
        == HVAC_SYS.SYS_9
    )


def test__is_baseline_system_9__test_json_true():
    assert (
        is_baseline_system_9(
            load_system_test_file("System_9_Warm_Air_Furnace_Gas.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 9",
            ["Air Terminal"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_9
    )


def test__is_baseline_system_9B_true():
    assert (
        is_baseline_system_9(
            SYS_9B_TEST_RMD["ruleset_model_descriptions"][0],
            "System 9B",
            ["Constant Air Terminal 9B"],
            ["Thermal Zone 9B"],
        )
        == HVAC_SYS.SYS_9B
    )


def test__is_baseline_system_9B__test_json_true():
    assert (
        is_baseline_system_9(
            load_system_test_file("System_9b_Warm_Air_Furnace_Gas.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 9B",
            ["Air Terminal"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_9B
    )
