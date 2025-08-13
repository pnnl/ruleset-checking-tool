from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_supply_return_exhaust_relief_terminal_fan_power_dict import (
    get_zone_supply_return_exhaust_relief_terminal_fan_power_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
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
                                    "primary_airflow": 1888,
                                }
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Zone exhaust fan 1",
                                    "specification_method": "SIMPLE",
                                    "design_electric_power": 20,
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "terminals": [
                                {
                                    "id": "PTAC Terminal 2-1",
                                    "is_supply_ducted": False,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "PTAC 2",
                                    "primary_airflow": 200,
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 3",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "terminals": [
                                {
                                    "id": "PTAC Terminal 3-1",
                                    "is_supply_ducted": False,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "PTAC 2",
                                    "primary_airflow": 800,
                                }
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Zone exhaust fan 1",
                                    "specification_method": "SIMPLE",
                                    "design_electric_power": 20,
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 4",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "terminals": [
                                {
                                    "id": "PTAC Terminal 4-1",
                                    "is_supply_ducted": False,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "PTAC 3",
                                    "primary_airflow": 800,
                                    "fan": {
                                        "id": "Terminal Supply Fan 1",
                                        "design_airflow": 500,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 10,
                                        "design_pressure_rise": 0.2,
                                    },
                                }
                            ],
                        },
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        # connect to thermal zone 1, one zone
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
                                "supply_fans": [
                                    {
                                        "id": "Supply Fan 1",
                                        "design_airflow": 500,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35,
                                        "design_pressure_rise": 0.2,
                                    },
                                ],
                                "relief_fans": [
                                    {
                                        "id": "Relief fan 1",
                                        "design_airflow": 200,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 15,
                                        "design_pressure_rise": 0.1,
                                    },
                                ],
                                "exhaust_fans": [
                                    {
                                        "id": "Exhaust fan 1",
                                        "design_airflow": 100,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35,
                                    },
                                ],
                                "return_fans": [
                                    {
                                        "id": "Return fan 1",
                                        "design_airflow": 700,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 30,
                                        "design_pressure_rise": 0.1,
                                    },
                                ],
                            },
                        },
                        # connect to thermal zone 2 and 3, primary airflow ratio is 2:8
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
                                "supply_fans": [
                                    {
                                        "id": "Supply Fan 2",
                                        "design_airflow": 500,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 10,
                                        "design_pressure_rise": 0.2,
                                    },
                                ],
                                "relief_fans": [
                                    {
                                        "id": "Relief fan 2",
                                        "design_airflow": 200,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 10,
                                        "design_pressure_rise": 0.1,
                                    },
                                ],
                                "exhaust_fans": [
                                    {
                                        "id": "Exhaust fan 2",
                                        "design_airflow": 100,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 10,
                                    },
                                ],
                                "return_fans": [
                                    {
                                        "id": "Return fan 2",
                                        "design_airflow": 700,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 10,
                                        "design_pressure_rise": 0.1,
                                    },
                                ],
                            },
                        },
                        # connect to thermal zone 4, no fan system
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

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_zone_supply_return_exhaust_relief_terminal_fan_power_dict_one_zone_one_terminal_success():
    zone_supply_return_exhaust_relief_terminal_fan_power_dict = (
        get_zone_supply_return_exhaust_relief_terminal_fan_power_dict(TEST_RMD)
    )
    # check supply fans
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 1"][
        "supply_fans_power"
    ] - 35 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 1"][
        "return_fans_power"
    ] - 30 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 1"][
        "exhaust_fans_power"
    ] - 55 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 1"][
        "relief_fans_power"
    ] - 15 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 1"][
        "terminal_fans_power"
    ] == 0.0 * ureg("W")


def test__get_zone_supply_return_exhaust_relief_terminal_fan_power_dict_two_zone_one_terminal_success():
    zone_supply_return_exhaust_relief_terminal_fan_power_dict = (
        get_zone_supply_return_exhaust_relief_terminal_fan_power_dict(TEST_RMD)
    )
    # check supply fans
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 2"][
        "supply_fans_power"
    ] - 2 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 2"][
        "return_fans_power"
    ] - 2 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 2"][
        "exhaust_fans_power"
    ] - 2 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 2"][
        "relief_fans_power"
    ] - 2 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 2"][
        "terminal_fans_power"
    ] == 0.0 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 3"][
        "supply_fans_power"
    ] - 8 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 3"][
        "return_fans_power"
    ] - 8 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 3"][
        "exhaust_fans_power"
    ] - 8 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 3"][
        "relief_fans_power"
    ] - 8 * ureg("W") < 0.001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 3"][
        "terminal_fans_power"
    ] == 0.0 * ureg("W")


def test__get_zone_supply_return_exhaust_relief_terminal_fan_power_dict_no_central_fan_success():
    zone_supply_return_exhaust_relief_terminal_fan_power_dict = (
        get_zone_supply_return_exhaust_relief_terminal_fan_power_dict(TEST_RMD)
    )
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 4"][
        "supply_fans_power"
    ] - 10 * ureg("W") < 0.0001 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 4"][
        "return_fans_power"
    ] == 0.0 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 4"][
        "exhaust_fans_power"
    ] == 0.0 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 4"][
        "relief_fans_power"
    ] == 0.0 * ureg("W")
    assert zone_supply_return_exhaust_relief_terminal_fan_power_dict["Thermal Zone 4"][
        "terminal_fans_power"
    ] - 10 * ureg("W") < 0.0001 * ureg("W")
