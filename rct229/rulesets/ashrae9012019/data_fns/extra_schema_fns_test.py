from copy import deepcopy

from rct229.rulesets.ashrae9012019.data_fns.extra_schema_fns import (
    compare_context_pair,
    EXTRA_SCHEMA,
)
from rct229.utils.json_utils import load_json

proposed = load_json(
    "C:\\Users\\xuwe123\\Documents\\GitHub\\ruleset-checking-tool\\examples\\chicago_demo\\proposed_model.json"
)
user = load_json(
    "C:\\Users\\xuwe123\\Documents\\GitHub\\ruleset-checking-tool\\examples\\chicago_demo\\user_model.json"
)
error_msg_list = []

TEST_RMI = {
    "id": "test_rmd",
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
                            "zonal_exhaust_fan": {
                                "id": "Zone exhaust fan 1",
                                "specification_method": "SIMPLE",
                                "design_electric_power": 200,
                                "design_airflow": 1500,
                            },
                        },
                        {
                            "id": "Thermal Zone 2",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "terminals": [
                                {
                                    "id": "PTAC Terminal 2",
                                    "is_supply_ducted": False,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "PTAC 2",
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 3",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "terminals": [
                                {
                                    "id": "PTAC Terminal 3",
                                    "is_supply_ducted": False,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "PTAC 3",
                                }
                            ],
                            "zonal_exhaust_fan": {
                                "id": "Zone exhaust fan 3-1",
                                "specification_method": "SIMPLE",
                                "design_electric_power": 200,
                                "design_airflow": 1500,
                            },
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
                                "exhaust_fans": [
                                    {
                                        "id": "Exhaust fan 1",
                                        "design_airflow": 1000,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35,
                                    },
                                    {
                                        "id": "Exhaust fan 2",
                                        "design_airflow": 500,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 25,
                                    },
                                ],
                            },
                        },
                        {
                            "id": "PTAC 2",
                            "cooling_system": {
                                "id": "DX Coil 2",
                                "type": "DIRECT_EXPANSION",
                            },
                            "heating_system": {
                                "id": "HHW Coil 2",
                                "type": "FLUID_LOOP",
                                "hot_water_loop": "Boiler Loop 1",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 2",
                                "fan_control": "CONSTANT",
                                "exhaust_fans": [
                                    {
                                        "id": "Exhaust fan 2-1",
                                        "design_airflow": 1000,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35,
                                    },
                                    {
                                        "id": "Exhaust fan 2-2",
                                        "design_airflow": 500,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 25,
                                    },
                                ],
                            },
                        },
                        {
                            "id": "PTAC 3",
                            "cooling_system": {
                                "id": "DX Coil 3",
                                "type": "DIRECT_EXPANSION",
                            },
                            "heating_system": {
                                "id": "HHW Coil 3",
                                "type": "FLUID_LOOP",
                                "hot_water_loop": "Boiler Loop 1",
                            },
                        },
                    ],
                }
            ],
        }
    ],
    "boilers": [
        {"id": "Boiler 1", "loop": "Boiler Loop 1", "energy_source_type": "NATURAL_GAS"}
    ],
    "fluid_loops": [{"id": "Boiler Loop 1", "type": "HEATING"}],
    "type": "BASELINE_0",
}


TEST_RMD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMI],
    "data_timestamp": "2024-02-12T09:00Z",
}


def test__compare_context_pair__identical():
    proposed = TEST_RMD_FULL
    user = TEST_RMD_FULL
    error_msg_list = []
    assert compare_context_pair(
        proposed,
        user,
        "$",
        EXTRA_SCHEMA["RulesetProjectDescription"]["Data Elements"],
        True,
        "AppG P_RMD Equals U_RMD",
        error_msg_list,
    )


def test__compare_context_pair__different():
    proposed = TEST_RMD_FULL
    user = deepcopy(TEST_RMD_FULL)
    user["ruleset_model_descriptions"][0]["buildings"][0][
        "building_open_schedule"
    ] = "always_1"
    error_msg_list = []
    assert not compare_context_pair(
        proposed,
        user,
        "$",
        EXTRA_SCHEMA["RulesetProjectDescription"]["Data Elements"],
        True,
        "AppG P_RMD Equals U_RMD",
        error_msg_list,
    )
    assert (
        error_msg_list[0]
        == "path: $.ruleset_model_descriptions[0].buildings[0].building_open_schedule: index context data: Required Building Schedule 1 does not equal to compare context data: always_1"
    )
