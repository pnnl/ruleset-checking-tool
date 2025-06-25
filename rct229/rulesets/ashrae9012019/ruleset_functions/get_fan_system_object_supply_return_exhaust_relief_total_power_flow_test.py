from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_system_object_supply_return_exhaust_relief_total_power_flow import (
    FanPressureDropCompareCategory,
    get_fan_system_object_supply_return_exhaust_relief_total_power_flow,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd
from rct229.utils.std_comparisons import std_equal

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
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Zone exhaust fan 1",
                                    "specification_method": "SIMPLE",
                                    "design_electric_power": 200,
                                }
                            ],
                        }
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
                                "supply_fans": [
                                    {
                                        "id": "Supply Fan 1",
                                        "design_airflow": 500,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35,
                                        "design_pressure_rise": 0.2,
                                    },
                                    {
                                        "id": "Supply Fan 2",
                                        "design_airflow": 600,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 50,
                                    },
                                    {
                                        "id": "Supply Fan 2",
                                        "design_airflow": 100,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 50,
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
                                    {
                                        "id": "Relief fan 1",
                                        "design_airflow": 100,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35,
                                        "design_pressure_rise": 0.05,
                                    },
                                ],
                                "exhaust_fans": [
                                    {
                                        "id": "Exhaust fan 1",
                                        "design_airflow": 100,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 35,
                                    },
                                    {
                                        "id": "Exhaust fan 2",
                                        "design_airflow": 50,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 25,
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
                                    {
                                        "id": "Return fan 2",
                                        "design_airflow": 60,
                                        "specification_method": "SIMPLE",
                                        "design_electric_power": 5,
                                        "design_pressure_rise": 0.1,
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

TEST_FAN_SYSTEM = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0][
    "buildings"
][0]["building_segments"][0]["heating_ventilating_air_conditioning_systems"][0][
    "fan_system"
]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM():
    all_fan_info = get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
        TEST_FAN_SYSTEM
    )
    # check supply fans
    assert std_equal(
        all_fan_info["supply_fans_power"],
        135 * ureg("W"),
    )

    assert std_equal(
        all_fan_info["supply_fans_airflow"],
        1200 * ureg("L/s"),
    )

    assert std_equal(
        all_fan_info["supply_fans_qty"],
        3,
    )

    assert (
        all_fan_info["supply_fans_pressure"] == FanPressureDropCompareCategory.UNDEFINED
    )

    # return fans
    assert std_equal(
        all_fan_info["return_fans_power"],
        35 * ureg("W"),
    )

    assert std_equal(
        all_fan_info["return_fans_airflow"],
        760 * ureg("L/s"),
    )

    assert std_equal(
        all_fan_info["return_fans_qty"],
        2,
    )

    assert (
        all_fan_info["return_fans_pressure"] == FanPressureDropCompareCategory.IDENTICAL
    )

    # relief fans
    assert std_equal(
        all_fan_info["relief_fans_power"],
        50 * ureg("W"),
    )

    assert std_equal(
        all_fan_info["relief_fans_airflow"],
        300 * ureg("L/s"),
    )

    assert std_equal(
        all_fan_info["relief_fans_qty"],
        2,
    )

    assert (
        all_fan_info["relief_fans_pressure"] == FanPressureDropCompareCategory.DIFFERENT
    )

    # exhaust fans
    assert std_equal(
        all_fan_info["exhaust_fans_power"],
        60 * ureg("W"),
    )

    assert std_equal(
        all_fan_info["exhaust_fans_airflow"],
        150 * ureg("L/s"),
    )

    assert std_equal(
        all_fan_info["exhaust_fans_qty"],
        2,
    )

    assert (
        all_fan_info["exhaust_fans_pressure"]
        == FanPressureDropCompareCategory.UNDEFINED
    )
