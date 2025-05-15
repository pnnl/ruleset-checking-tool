from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_10 import (
    is_baseline_system_10,
)
from rct229.schema.validate import schema_validate_rpd

# The first logic means the first half of the `is_baseline_system_10'. The first logic is used when there are NO preheat/heating and fan systems.
# The second logic means the second half of the `is_baseline_system_10'. The second logic is used when there is NO preheat system and there is heating/fan systems.
SYS_10_FIRST_LOGIC_TEST_RMD = {
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
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 10",
                                            "heating_source": "ELECTRIC",
                                            "fan": {"id": "Terminal Fan 1"},
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 10",
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


SYS_10_SECOND_LOGIC_TEST_RMD = {
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
                                    "id": "Thermal Zone 2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 2",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 10",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 10",
                                    "cooling_system": {
                                        "id": "Cooling Coil 1",
                                        "type": "NONE",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1A",
                                        "type": "ELECTRIC_RESISTANCE",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1",
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


def test__TEST_RMD_baseline_system_10__is_first_logic_valid():
    schema_validation_result = schema_validate_rpd(SYS_10_FIRST_LOGIC_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_baseline_system_10__is_second_logic_valid():
    schema_validation_result = schema_validate_rpd(SYS_10_FIRST_LOGIC_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline_system_10__first_logic_true():
    assert (
        is_baseline_system_10(
            SYS_10_FIRST_LOGIC_TEST_RMD["ruleset_model_descriptions"][0],
            "System 10",
            ["Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_10
    )


def test__is_baseline_system_10__second_logic_true():
    assert (
        is_baseline_system_10(
            SYS_10_SECOND_LOGIC_TEST_RMD["ruleset_model_descriptions"][0],
            "System 10",
            ["Air Terminal 2"],
            ["Thermal Zone 2"],
        )
        == HVAC_SYS.SYS_10
    )


def test__is_baseline_system_10__test_json_true():
    assert (
        is_baseline_system_10(
            load_system_test_file("System_10_Warm_Air_Furnace_Elec.json")[
                "ruleset_model_descriptions"
            ][0],
            "System 10",
            ["Air Terminal"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_10
    )
