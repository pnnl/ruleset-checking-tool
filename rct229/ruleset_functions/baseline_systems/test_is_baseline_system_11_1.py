from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.is_baseline_system_11_1 import (
    is_baseline_system_11_1,
)

rmd_model = {
    "id": "ASHRAE229 1",
    "ruleset_model_instances": [
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
                                            "served_by_heating_ventilation_air_conditioning_system": "System Type 11B",
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
                                            "served_by_heating_ventilation_air_conditioning_system": "System Type 11",
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
                                            "served_by_heating_ventilation_air_conditioning_system": "System Type 11A",
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
                                            "served_by_heating_ventilation_air_conditioning_system": "System Type 11C",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilation_air_conditioning_systems": [
                                {
                                    "id": "System Type 11B",
                                    "cooling_system": {
                                        "id": "CHW Coil 1B",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chiller Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1B",
                                        "heating_system_type": "FLUID_LOOP",
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
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chiller Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1",
                                        "heating_system_type": "ELECTRIC_RESISTANCE",
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
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1A",
                                        "heating_system_type": "ELECTRIC_RESISTANCE",
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
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1C",
                                        "heating_system_type": "FLUID_LOOP",
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
            "external_fluid_source": [
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
                {"id": "Chiller Loop 1", "type": "COOLING"},
                {
                    "id": "Purchased CHW Loop 1",
                    "type": "COOLING",
                },
            ],
        }
    ],
}


def test_is_baseline__system_11_1():
    assert (
        is_baseline_system_11_1(
            rmd_model["ruleset_model_instances"][0],
            "System Type 11",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_11_1
    )


def test_is_baseline__system__11_1A():
    assert (
        is_baseline_system_11_1(
            rmd_model["ruleset_model_instances"][0],
            "System Type 11A",
            ["VAV Air Terminal 1A"],
            ["Thermal Zone 1A"],
        )
        == HVAC_SYS.SYS_11_1A
    )


def test_is_baseline__system_11_1B():
    assert (
        is_baseline_system_11_1(
            rmd_model["ruleset_model_instances"][0],
            "System Type 11B",
            ["VAV Air Terminal 1B"],
            ["Thermal Zone 1B"],
        )
        == HVAC_SYS.SYS_11_1B
    )


def test_is_baseline__system_11_1C():
    assert (
        is_baseline_system_11_1(
            rmd_model["ruleset_model_instances"][0],
            "System Type 11C",
            ["VAV Air Terminal 1C"],
            ["Thermal Zone 1C"],
        )
        == HVAC_SYS.SYS_11_1C
    )
