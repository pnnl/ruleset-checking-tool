from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zone_peak_internal_load_floor_area_dict import (
    get_zone_peak_internal_load_floor_area_dict,
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
                        # this zone shall give a total floor area of 500
                        # total zone peak load of 1500 W
                        {
                            "id": "Thermal Zone 1",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "spaces": [
                                {
                                    "id": "space 1",
                                    "floor_area": 500,
                                    "interior_lighting": [
                                        {
                                            "id": "interior_lighting_1",
                                            "lighting_multiplier_schedule": "lighting_schedule_1",
                                            "power_per_area": 1.0,
                                        }
                                    ],
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "miscellaneous_equipment_1",
                                            "multiplier_schedule": "miscellaneous_equipment_schedule_1",
                                            "power": 500,
                                        }
                                    ],
                                    "occupant_multiplier_schedule": "occupant_schedule_1",
                                    "occupant_sensible_heat_gain": 125,
                                    "occupant_latent_heat_gain": 125,
                                }
                            ],
                        },
                        # this zone shall give a total floor area of 500
                        # total zone peak load of 1000 W due to no lights
                        {
                            "id": "Thermal Zone 2",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "spaces": [
                                {
                                    "id": "space 2",
                                    "floor_area": 500,
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "miscellaneous_equipment_1",
                                            "multiplier_schedule": "miscellaneous_equipment_schedule_1",
                                            "power": 500,
                                        }
                                    ],
                                    "occupant_multiplier_schedule": "occupant_schedule_1",
                                    "occupant_sensible_heat_gain": 125,
                                    "occupant_latent_heat_gain": 125,
                                }
                            ],
                        },
                        # this zone shall give a total floor area of 500
                        # total zone peak load of 1000 W due to no occupants
                        {
                            "id": "Thermal Zone 3",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "spaces": [
                                {
                                    "id": "space 3",
                                    "floor_area": 500,
                                    "interior_lighting": [
                                        {
                                            "id": "interior_lighting_1",
                                            "lighting_multiplier_schedule": "lighting_schedule_1",
                                            "power_per_area": 1.0,
                                        }
                                    ],
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "miscellaneous_equipment_1",
                                            "multiplier_schedule": "miscellaneous_equipment_schedule_1",
                                            "power": 500,
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            # this zone has no space, space area is 0
                            # total zone peak load of 0 W
                            "id": "Thermal Zone 4",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                        },
                    ],
                },
            ],
        }
    ],
    "schedules": [
        {"id": "lighting_schedule_1", "hourly_cooling_design_day": [1] * 24},
        {
            "id": "miscellaneous_equipment_schedule_1",
            "hourly_cooling_design_day": [1] * 24,
        },
        {"id": "occupant_schedule_1", "hourly_cooling_design_day": [1] * 23 + [2]},
    ],
    "type": "BASELINE_0",
}


TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
}

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_zone_peak_internal_load_floor_area_dict__all_three_component():
    zone_info = get_zone_peak_internal_load_floor_area_dict(TEST_RMD, "Thermal Zone 1")
    assert abs(zone_info["peak"] - 1500 * ureg("watt")) < 0.00001 * ureg("watt")
    assert abs(zone_info["area"] - 500 * ureg("m2")) < 0.00001 * ureg("m2")


def test__get_zone_peak_internal_load_floor_area_dict__no_lighting_component():
    zone_info = get_zone_peak_internal_load_floor_area_dict(TEST_RMD, "Thermal Zone 2")
    assert abs(zone_info["peak"] - 1000 * ureg("watt")) < 0.00001 * ureg("watt")
    assert abs(zone_info["area"] - 500 * ureg("m2")) < 0.00001 * ureg("m2")


def test__get_zone_peak_internal_load_floor_area_dict__no_occupants_component():
    zone_info = get_zone_peak_internal_load_floor_area_dict(TEST_RMD, "Thermal Zone 3")
    assert abs(zone_info["peak"] - 1000 * ureg("watt")) < 0.00001 * ureg("watt")
    assert abs(zone_info["area"] - 500 * ureg("m2")) < 0.00001 * ureg("m2")


def test__get_zone_peak_internal_load_floor_area_dict__no_space_component():
    zone_info = get_zone_peak_internal_load_floor_area_dict(TEST_RMD, "Thermal Zone 4")
    assert abs(zone_info["peak"] - 0 * ureg("watt")) < 0.00001 * ureg("watt")
    assert abs(zone_info["area"] - 0 * ureg("m2")) < 0.00001 * ureg("m2")
