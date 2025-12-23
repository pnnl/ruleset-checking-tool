from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_sys_and_assoc_zones_largest_exhaust_source import (
    get_hvac_sys_and_assoc_zones_largest_exhaust_source,
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
                                }
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Zone exhaust fan 1",
                                    "specification_method": "SIMPLE",
                                    "design_electric_power": 200,
                                    "design_airflow": 1500,
                                }
                            ],
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
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Zone exhaust fan 3-1",
                                    "specification_method": "SIMPLE",
                                    "design_electric_power": 200,
                                    "design_airflow": 1500,
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


def test_get_hvac_sys_and_assoc_zones_largest_exhaust_source_hvac_and_zone_success():
    hvac_sys_and_assoc_zones_largest_exhaust_source_dict = (
        get_hvac_sys_and_assoc_zones_largest_exhaust_source(TEST_RMD_UNIT, "PTAC 1")
    )
    assert hvac_sys_and_assoc_zones_largest_exhaust_source_dict[
        "hvac_fan_sys_exhaust_sum"
    ] - 1500 * ureg("liter / second") < 0.001 * ureg("liter / second")

    assert hvac_sys_and_assoc_zones_largest_exhaust_source_dict[
        "maximum_zone_exhaust"
    ] - 1500 * ureg("liter / second") < 0.001 * ureg("liter / second")

    assert (
        hvac_sys_and_assoc_zones_largest_exhaust_source_dict["num_hvac_exhaust_fans"]
        == 2
    )

    assert hvac_sys_and_assoc_zones_largest_exhaust_source_dict[
        "maximum_hvac_exhaust"
    ] - 1000 * ureg("liter / second") < 0.001 * ureg("liter / second")


def test_get_hvac_sys_and_assoc_zones_largest_exhaust_source_hvac_only_success():
    hvac_sys_and_assoc_zones_largest_exhaust_source_dict = (
        get_hvac_sys_and_assoc_zones_largest_exhaust_source(TEST_RMD_UNIT, "PTAC 2")
    )
    assert hvac_sys_and_assoc_zones_largest_exhaust_source_dict[
        "hvac_fan_sys_exhaust_sum"
    ] - 1500 * ureg("liter / second") < 0.001 * ureg("liter / second")

    assert hvac_sys_and_assoc_zones_largest_exhaust_source_dict[
        "maximum_zone_exhaust"
    ] == 0.0 * ureg("liter / second")

    assert (
        hvac_sys_and_assoc_zones_largest_exhaust_source_dict["num_hvac_exhaust_fans"]
        == 2
    )

    assert hvac_sys_and_assoc_zones_largest_exhaust_source_dict[
        "maximum_hvac_exhaust"
    ] - 1000 * ureg("liter / second") < 0.001 * ureg("liter / second")


def test_get_hvac_sys_and_assoc_zones_largest_exhaust_source_zone_only_success():
    hvac_sys_and_assoc_zones_largest_exhaust_source_dict = (
        get_hvac_sys_and_assoc_zones_largest_exhaust_source(TEST_RMD_UNIT, "PTAC 3")
    )
    assert hvac_sys_and_assoc_zones_largest_exhaust_source_dict[
        "hvac_fan_sys_exhaust_sum"
    ] == 0.0 * ureg("liter / second")

    assert hvac_sys_and_assoc_zones_largest_exhaust_source_dict[
        "maximum_zone_exhaust"
    ] - 1500 * ureg("liter / second") < 0.001 * ureg("liter / second")

    assert (
        hvac_sys_and_assoc_zones_largest_exhaust_source_dict["num_hvac_exhaust_fans"]
        == 0
    )

    assert hvac_sys_and_assoc_zones_largest_exhaust_source_dict[
        "maximum_hvac_exhaust"
    ] == 0.0 * ureg("liter / second")
