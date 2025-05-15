# hvac_id = "PTAC 1" => Sys_1, [Thermal Zone 1], [PTAC Terminal 1]
# hvac_id = "PTAC 1a" => Sys_1a, [Thermal Zone 1a], [PTAC Terminal 1a]
# hvac_id = "PTAC 1b" => Sys_1b, [Thermal Zone 1b], [PTAC Terminal 1b]
# hvac_id = "PTAC 1c" => Sys_1c, [Thermal Zone 1c], [PTAC Terminal 1c]
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_1 import (
    is_baseline_system_1,
)
from rct229.schema.validate import schema_validate_rpd

SYS_1_TEST_RMD = {
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
                                            "id": "PTAC Terminal 1",
                                            "is_supply_ducted": False,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "PTAC 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1b",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "PTAC Terminal 1b",
                                            "is_supply_ducted": False,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "PTAC 1b",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1a",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "PTAC Terminal 1a",
                                            "is_supply_ducted": False,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "fan": {"id": "fan 1a"},
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Boiler Loop 1",
                                            "cooling_source": "CHILLED_WATER",
                                            "cooling_from_loop": "Purchased CHW Loop 1",
                                            # this is necessary in the current setup.
                                            # This parameter connects hvac_b with specific terminal so that the
                                            # function is_baseline_system_1 can execute within the correct zone list.
                                            "served_by_heating_ventilating_air_conditioning_system": "PTAC 1a",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1c",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "PTAC Terminal 1c",
                                            "is_supply_ducted": False,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "fan": {"id": "fan 1c"},
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "cooling_source": "CHILLED_WATER",
                                            "cooling_from_loop": "Purchased CHW Loop 1",
                                            # this is necessary in the current setup.
                                            # This parameter connects hvac_b with specific terminal so that the
                                            # function is_baseline_system_1 can execute within the correct zone list.
                                            "served_by_heating_ventilating_air_conditioning_system": "PTAC 1c",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "PTAC 1",
                                    "cooling_system": {
                                        "id": "DX Coil 1",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                    },
                                },
                                {
                                    "id": "PTAC 1b",
                                    "cooling_system": {
                                        "id": "DX Coil 1b",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1b",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1b",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1b"}],
                                    },
                                },
                                {
                                    "id": "PTAC 1a",
                                },
                                {
                                    "id": "PTAC 1c",
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
                    "condensing_loop": "Condenser Loop 1",
                }
            ],
            "boilers": [
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "energy_source_type": "NATURAL_GAS",
                }
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
                    "id": "Purchased HW Loop 1",
                    "type": "HEATING",
                },
                {
                    "id": "Purchased CHW Loop 1",
                    "type": "COOLING",
                },
                {
                    "id": "Chiller Loop 1",
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


def test__TEST_RMD_baseline_system_1__is_valid():
    schema_validation_result = schema_validate_rpd(SYS_1_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline_system_1__true():
    assert (
        is_baseline_system_1(
            SYS_1_TEST_RMD["ruleset_model_descriptions"][0],
            "PTAC 1",
            ["PTAC Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_1
    )


def test__is_baseline_system_1A__true():
    assert (
        is_baseline_system_1(
            SYS_1_TEST_RMD["ruleset_model_descriptions"][0],
            "PTAC 1a",
            ["PTAC Terminal 1a"],
            ["Thermal Zone 1a"],
        )
        == HVAC_SYS.SYS_1A
    )


def test__is_baseline_system_1A__test_json_true():
    assert (
        is_baseline_system_1(
            load_system_test_file("System_1a_PTAC.json")["ruleset_model_descriptions"][
                0
            ],
            "PTAC 1",
            ["PTAC Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_1A
    )


def test__is_baseline_system_1B__true():
    assert (
        is_baseline_system_1(
            SYS_1_TEST_RMD["ruleset_model_descriptions"][0],
            "PTAC 1b",
            ["PTAC Terminal 1b"],
            ["Thermal Zone 1b"],
        )
        == HVAC_SYS.SYS_1B
    )


def test__is_baseline_system_1B__test_json_true():
    assert (
        is_baseline_system_1(
            load_system_test_file("System_1b_PTAC.json")["ruleset_model_descriptions"][
                0
            ],
            "PTAC 1",
            ["PTAC Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_1B
    )


def test__is_baseline_system_1C__true():
    assert (
        is_baseline_system_1(
            SYS_1_TEST_RMD["ruleset_model_descriptions"][0],
            "PTAC 1c",
            ["PTAC Terminal 1c"],
            ["Thermal Zone 1c"],
        )
        == HVAC_SYS.SYS_1C
    )


def test__is_baseline_system_1__test_json_true():
    assert (
        is_baseline_system_1(
            load_system_test_file("System_1_PTAC.json")["ruleset_model_descriptions"][
                0
            ],
            "PTAC 1",
            ["PTAC Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_1
    )


def test__is_baseline_system_1C__test_json_true():
    assert (
        is_baseline_system_1(
            load_system_test_file("System_1c_PTAC.json")["ruleset_model_descriptions"][
                0
            ],
            "PTAC 1",
            ["PTAC Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_1C
    )
