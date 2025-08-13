from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_5_6_serving_multiple_floors import (
    get_hvac_systems_5_6_serving_multiple_floors,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "Test RMD",
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
                            "floor_name": "Floor 1",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "terminals": [
                                {
                                    "id": "VAV Air Terminal 1",
                                    "is_supply_ducted": True,
                                    "type": "VARIABLE_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 5",
                                    "heating_source": "HOT_WATER",
                                    "heating_from_loop": "Boiler Loop 1",
                                    "minimum_outdoor_airflow": 14.158423295999995,
                                    "minimum_outdoor_airflow_multiplier_schedule": "Min OA CFM Schedule",
                                }
                            ],
                            "spaces": [{"id": "Space 1", "floor_area": 1000}],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "floor_name": "Floor 2",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "terminals": [
                                {
                                    "id": "VAV Air Terminal 2",
                                    "is_supply_ducted": True,
                                    "type": "VARIABLE_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 5",
                                    "heating_source": "HOT_WATER",
                                    "heating_from_loop": "Boiler Loop 1",
                                    "minimum_outdoor_airflow": 14.158423295999995,
                                    "minimum_outdoor_airflow_multiplier_schedule": "Min OA CFM Schedule",
                                }
                            ],
                            "spaces": [{"id": "Space 2", "floor_area": 1000}],
                        },
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 5",
                            "cooling_system": {
                                "id": "DX Coil 1",
                                "type": "DIRECT_EXPANSION",
                            },
                            "preheat_system": {
                                "id": "Preheat Coil 1",
                                "type": "FLUID_LOOP",
                                "hot_water_loop": "Boiler Loop 1",
                            },
                            "fan_system": {
                                "id": "VAV Fan System 1",
                                "fan_control": "VARIABLE_SPEED_DRIVE",
                                "supply_fans": [{"id": "Supply Fan 1"}],
                                "return_fans": [{"id": "Return Fan 1"}],
                                "minimum_outdoor_airflow": 1887.7897727999994,
                            },
                        }
                    ],
                }
            ],
        }
    ],
    "boilers": [
        {"id": "Boiler 1", "loop": "Boiler Loop 1", "energy_source_type": "NATURAL_GAS"}
    ],
    "pumps": [
        {
            "id": "Boiler Pump 1",
            "loop_or_piping": "Boiler Loop 1",
            "speed_control": "FIXED_SPEED",
        }
    ],
    "fluid_loops": [{"id": "Boiler Loop 1", "type": "HEATING"}],
    "type": "BASELINE_0",
}


TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RMD_UNIT = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_hvac_systems_5_6_serving_multiple_floors():
    hvac_systems_5_6_serving_multiple_floors = (
        get_hvac_systems_5_6_serving_multiple_floors(TEST_RMD_UNIT)
    )
    assert hvac_systems_5_6_serving_multiple_floors == {
        "System 5": 2
    }, f"Expected: {{'System 5': 2}}, Actual: {hvac_systems_5_6_serving_multiple_floors}"
