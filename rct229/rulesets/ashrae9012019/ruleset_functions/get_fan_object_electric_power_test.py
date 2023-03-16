from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_object_electric_power import (
    get_fan_object_electric_power,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

TEST_RMD = {
    "id": "ASHRAE229 1",
    "ruleset_model_instances": [
        {
            "id": "RMI 1",
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
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 2",
                                            "is_supply_ducted": True,
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 7",
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chilled Water Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [
                                            {
                                                "id": "Supply Fan 1",
                                                "specification_method": "SIMPLE",
                                                "design_electric_power": 100,
                                            },
                                            {
                                                "id": "Supply Fan 2",
                                                "specification_method": "DETAILED",
                                                "input_power": 100,
                                                "motor_efficiency": 0.5,
                                            },
                                            # 0.00397677575 Btu/hr -> 0.00116620989 watt
                                            {
                                                "id": "Supply Fan 3",
                                                "specification_method": "DETAILED",
                                                "design_pressure_rise": 5,
                                                "total_efficiency": 0.5,
                                            },
                                            {
                                                "id": "Supply Fan 4",
                                                "specification_method": "DETAILED",
                                                "total_efficiency": 0.5,
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
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "energy_source_type": "NATURAL_GAS",
                }
            ],
            "chillers": [{"id": "Chiller 1", "cooling_loop": "Chiller Loop 1"}],
            "pumps": [
                {
                    "id": "Boiler Pump 1",
                    "loop_or_piping": "Boiler Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "Chiller Pump 1",
                    "loop_or_piping": "Chiller Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
            ],
            "fluid_loops": [
                {"id": "Boiler Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Chilled Water Loop 1", "type": "COOLING"}],
                },
            ],
        }
    ],
}


TEST_RMI = quantify_rmr(TEST_RMD)["ruleset_model_instances"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__FAN_SIMPLE__success():
    fan = find_exactly_one_with_field_value(
        "$.buildings[0].building_segments["
        "0].heating_ventilating_air_conditioning_systems["
        "0].fan_system.supply_fans[*]",
        "id",
        "Supply Fan 1",
        TEST_RMI,
    )
    assert get_fan_object_electric_power(fan) == 100 * ureg("watt")


def test__FAN_DETAIL_motor_efficiency__success():
    fan = find_exactly_one_with_field_value(
        "$.buildings[0].building_segments["
        "0].heating_ventilating_air_conditioning_systems["
        "0].fan_system.supply_fans[*]",
        "id",
        "Supply Fan 2",
        TEST_RMI,
    )
    assert get_fan_object_electric_power(fan) == 200 * ureg("watt")


def test__FAN_DETAIL_total_efficiency__success():
    fan = find_exactly_one_with_field_value(
        "$.buildings[0].building_segments["
        "0].heating_ventilating_air_conditioning_systems["
        "0].fan_system.supply_fans[*]",
        "id",
        "Supply Fan 3",
        TEST_RMI,
    )
    assert abs(
        get_fan_object_electric_power(fan) - 0.00116 * ureg("watt")
    ) < 0.000006 * ureg("watt")


def test_FAN_MISSING_DATA_FAILED():
    fan = find_exactly_one_with_field_value(
        "$.buildings[0].building_segments["
        "0].heating_ventilating_air_conditioning_systems["
        "0].fan_system.supply_fans[*]",
        "id",
        "Supply Fan 4",
        TEST_RMI,
    )
    assert get_fan_object_electric_power(fan) == None
