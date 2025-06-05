import json
import os
from pathlib import Path

from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd
from rct229.utils.utility_functions import (
    has_cooling_system,
    has_fan_system,
    has_heating_system,
    has_preheat_system,
)

SYSTEM_TYPE_TEST_FILE_PATH = os.path.join(
    Path(os.path.dirname(__file__)).parent.parent.parent.parent,
    "ruletest_engine",
    "ruletest_jsons",
    "ashrae9012019",
    "system_types",
)


def load_system_test_file(file_name: str):
    with open(os.path.join(SYSTEM_TYPE_TEST_FILE_PATH, file_name)) as f:
        system_test_json = json.load(f)

    assert system_test_json, f"Error loading system testing json file: #{file_name}"
    return quantify_rmd(system_test_json)


TEST_RMD_PASS = {
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
                                            "id": "PTHP Terminal 1",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "PTHP 1",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "PTHP 1",
                                    "cooling_system": {
                                        "id": "HP Cooling Coil 1",
                                        "type": "DIRECT_EXPANSION",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "type": "ELECTRIC_RESISTANCE",
                                    },
                                    "heating_system": {
                                        "id": "HP Heating Coil 1",
                                        "type": "HEAT_PUMP",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                    },
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ],
}

TEST_RMD_FAIL = {
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
                                            "id": "PTHP Terminal 1",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "PTHP 1",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "PTHP 1",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ],
}


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_PASS)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_has_heating_system_true():
    assert (
        has_heating_system(TEST_RMD_PASS["ruleset_model_descriptions"][0], "PTHP 1")
        == True
    )


def test_has_heating_system_fail():
    assert (
        has_heating_system(TEST_RMD_FAIL["ruleset_model_descriptions"][0], "PTHP 1")
        == False
    )


def test_has_cooling_system_true():
    assert (
        has_cooling_system(TEST_RMD_PASS["ruleset_model_descriptions"][0], "PTHP 1")
        == True
    )


def test_has_cooling_system_fail():
    assert (
        has_cooling_system(TEST_RMD_FAIL["ruleset_model_descriptions"][0], "PTHP 1")
        == False
    )


def test_has_preheat_system_true():
    assert (
        has_preheat_system(TEST_RMD_PASS["ruleset_model_descriptions"][0], "PTHP 1")
        == True
    )


def test_has_preheat_system_fail():
    assert (
        has_preheat_system(TEST_RMD_FAIL["ruleset_model_descriptions"][0], "PTHP 1")
        == False
    )


def test_has_fan_system_true():
    assert (
        has_fan_system(TEST_RMD_PASS["ruleset_model_descriptions"][0], "PTHP 1") == True
    )


def test_has_fan_system_fail():
    assert (
        has_fan_system(TEST_RMD_FAIL["ruleset_model_descriptions"][0], "PTHP 1")
        == False
    )
