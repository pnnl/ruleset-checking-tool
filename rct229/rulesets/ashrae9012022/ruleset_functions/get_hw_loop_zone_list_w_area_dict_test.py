from rct229.rulesets.ashrae9012019.ruleset_functions.get_hw_loop_zone_list_w_area_dict import (
    get_hw_loop_zone_list_w_area,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

GET_HW_LOOP_ZONE_LIST_W_AREA_RMD = {
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
                                            "heating_from_loop": "Boiler Loop 1",
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                        }
                                    ],
                                    "spaces": [{"id": "Space 1", "floor_area": 10}],
                                },
                                {
                                    "id": "Thermal Zone 2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 2",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                        }
                                    ],
                                    "spaces": [
                                        {
                                            "id": "Space 2",
                                            "floor_area": 20,
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 3",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 3",
                                            "is_supply_ducted": True,
                                            "served_by_heating_ventilating_air_conditioning_system": "PTAC 1",
                                        }
                                    ],
                                    "spaces": [
                                        {
                                            "id": "Space 3",
                                            "floor_area": 30,
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 4",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 4",
                                            "is_supply_ducted": True,
                                            # intentionally omitted `served_by_heating_ventilating_air_conditioning_system` key to test the `elif terminal.get("served_by_heating_ventilating_air_conditioning_system"):` condition
                                        }
                                    ],
                                    "spaces": [
                                        {
                                            "id": "Space 4",
                                            "floor_area": 30,
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 5",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 5",
                                            "is_supply_ducted": True,
                                            "served_by_heating_ventilating_air_conditioning_system": "Electric Resistance System",
                                        }
                                    ],
                                    "spaces": [
                                        {
                                            "id": "Space 5",
                                            "floor_area": 30,
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 7",
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "cooling_system": {
                                        "id": "Cooling Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chiller Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
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
                                    "id": "Electric Resistance System",
                                    "heating_system": {
                                        "id": "Resistance 1",
                                        "type": "ELECTRIC_RESISTANCE",
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
                    "design_capacity": 117228.44444444445,
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

TEST_RMD = quantify_rmd(GET_HW_LOOP_ZONE_LIST_W_AREA_RMD)["ruleset_model_descriptions"][
    0
]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(GET_HW_LOOP_ZONE_LIST_W_AREA_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_hw_loop_zone_list_w_area__true():
    assert get_hw_loop_zone_list_w_area(TEST_RMD) == {
        "Boiler Loop 1": {
            "zone_list": ["Thermal Zone 1", "Thermal Zone 2", "Thermal Zone 3"],
            "total_area": 60 * ureg.m2,
        }
    }
