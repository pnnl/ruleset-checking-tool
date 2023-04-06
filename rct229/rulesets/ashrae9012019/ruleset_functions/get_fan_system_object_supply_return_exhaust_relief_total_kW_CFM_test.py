from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM import (
    get_fan_system_object_supply_return_exhaust_relief_total_kw_cfm,
)
from rct229.schema.config import ureg

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
                                }
                            ],
                            "zonal_exhaust_fan": {
                                "id": "Zone exhaust fan 1",
                                "specification_method": "SIMPLE",
                                "design_electric_power": 200,
                            },
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "PTAC 1",
                            "cooling_system": {
                                "id": "DX Coil 1",
                                "cooling_system_type": "DIRECT_EXPANSION",
                            },
                            "heating_system": {
                                "id": "HHW Coil 1",
                                "heating_system_type": "FLUID_LOOP",
                                "hot_water_loop": "Boiler Loop 1",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 1",
                                "fan_control": "CONSTANT",
                                "supply_fans": [
                                    {
                                        "id": "Supply Fan 1",
                                        "design_airflow": 500 * ureg("cfm"),
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35 * ureg("W"),
                                        "design_pressure_rise": 0.2 * ureg("W"),
                                    },
                                    {
                                        "id": "Supply Fan 2",
                                        "design_airflow": 600 * ureg("cfm"),
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 50 * ureg("W"),
                                    },
                                    {
                                        "id": "Supply Fan 2",
                                        "design_airflow": 100 * ureg("cfm"),
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 50 * ureg("W"),
                                    },
                                ],
                                "relief_fans": [
                                    {
                                        "id": "Relief fan 1",
                                        "design_airflow": 200 * ureg("cfm"),
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 15 * ureg("W"),
                                        "design_pressure_rise": 0.1 * ureg("W"),
                                    },
                                    {
                                        "id": "Relief fan 1",
                                        "design_airflow": 100 * ureg("cfm"),
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35 * ureg("W"),
                                        "design_pressure_rise": 0.05 * ureg("W"),
                                    },
                                ],
                                "exhaust_fans": [
                                    {
                                        "id": "Exhaust fan 1",
                                        "design_airflow": 100 * ureg("cfm"),
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35 * ureg("W"),
                                    },
                                    {
                                        "id": "Exhaust fan 2",
                                        "design_airflow": 50 * ureg("cfm"),
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 25 * ureg("W"),
                                    },
                                ],
                                "return_fans": [
                                    {
                                        "id": "Return fan 1",
                                        "design_airflow": 700 * ureg("cfm"),
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 30 * ureg("W"),
                                        "design_pressure_rise": 0.1 * ureg("W"),
                                    },
                                    {
                                        "id": "Return fan 2",
                                        "design_airflow": 60 * ureg("cfm"),
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 5 * ureg("W"),
                                        "design_pressure_rise": 0.1 * ureg("W"),
                                    },
                                ],
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
    "fluid_loops": [{"id": "Boiler Loop 1", "type": "HEATING"}],
}


def test__get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM():
    assert get_fan_system_object_supply_return_exhaust_relief_total_kw_cfm(
        TEST_RMD["buildings"][0]["building_segments"][0][
            "heating_ventilating_air_conditioning_systems"
        ][0]["fan_system"]
    ) == {
        "supply_fans_power": 135.0 * ureg("W"),
        "supply_fans_cfm": 1200.0 * ureg("cfm"),
        "supply_fans_qty": 3,
        "supply_fans_pressure": "UNDEFINED",
        "return_fans_power": 35.0 * ureg("W"),
        "return_fans_cfm": 760.0 * ureg("cfm"),
        "return_fans_qty": 2,
        "return_fans_pressure": "IDENTICAL",
        "exhaust_fans_power": 60.0 * ureg("W"),
        "exhaust_fans_cfm": 150.0 * ureg("cfm"),
        "exhaust_fans_qty": 2,
        "exhaust_fans_pressure": "UNDEFINED",
        "relief_fans_power": 50.0 * ureg("W"),
        "relief_fans_cfm": 300.0 * ureg("cfm"),
        "relief_fans_qty": 2,
        "relief_fans_pressure": "DIFFERENT",
    }
