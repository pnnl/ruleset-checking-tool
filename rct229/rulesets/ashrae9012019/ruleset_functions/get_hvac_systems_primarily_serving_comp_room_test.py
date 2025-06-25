from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_primarily_serving_comp_room import (
    get_hvac_systems_primarily_serving_comp_room,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                {
                    "id": "bldg_seg_1",
                    "heating_ventilating_air_conditioning_systems": [
                        {"id": "hvac_1"},
                        {"id": "hvac_2"},
                    ],
                    "zones": [
                        {
                            "id": "zone_1",
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "spaces": [
                                {
                                    "id": "space_1_1",
                                    "floor_area": 1000,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "number_of_occupants": 10,
                                    "occupant_sensible_heat_gain": 100,
                                    "occupant_multiplier_schedule": "occ_mul_sched_1",
                                    "interior_lighting": [
                                        {
                                            "id": "int_lighting_1",
                                            "power_per_area": 0.41,
                                            "daylighting_control_type": "NONE",
                                            "lighting_multiplier_schedule": "lgt_mul_sche_1",
                                        }
                                    ],
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "miscellaneous_equipment_1",
                                            "multiplier_schedule": "misc_equip_schedule_1",
                                            "power": 5000,
                                        }
                                    ],
                                },
                                {
                                    "id": "space_1_2",
                                    "floor_area": 500,  # m2
                                    "number_of_occupants": 10,
                                    "occupant_sensible_heat_gain": 100,
                                    "occupant_multiplier_schedule": "occ_mul_sched_1",
                                    "interior_lighting": [
                                        {
                                            "id": "int_lighting_2",
                                            "power_per_area": 0.41,
                                            "daylighting_control_type": "NONE",
                                            "lighting_multiplier_schedule": "lgt_mul_sche_1",
                                        }
                                    ],
                                    "miscellaneous_equipment": [
                                        {
                                            "id": "miscellaneous_equipment_2",
                                            "multiplier_schedule": "misc_equip_schedule_1",
                                            "power": 5000,
                                        }
                                    ],
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_1_1_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1",
                                },
                                {
                                    "id": "terminal_1_1_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1",
                                },
                            ],
                        },
                        {
                            "id": "zone_2",
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "spaces": [
                                {
                                    "id": "space_2_1",
                                    "floor_area": 300,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "occ_mul_sched_1",
                                    "interior_lighting": [
                                        {
                                            "id": "int_lighting_2",
                                            "power_per_area": 0.41,
                                            "daylighting_control_type": "NONE",
                                            "lighting_multiplier_schedule": "lgt_mul_sche_1",
                                        }
                                    ],
                                },
                                {
                                    "id": "space_2_2",
                                    "floor_area": 1000,  # m2
                                    "occupant_multiplier_schedule": "occ_mul_sched_1",
                                    "interior_lighting": [
                                        {
                                            "id": "int_lighting_2",
                                            "power_per_area": 0.41,
                                            "daylighting_control_type": "NONE",
                                            "lighting_multiplier_schedule": "lgt_mul_sche_1",
                                        }
                                    ],
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_2_1_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2",
                                },
                                {
                                    "id": "terminal_2_1_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2",
                                },
                            ],
                        },
                    ],
                }
            ],
        }
    ],
    "schedules": [
        {
            "id": "occ_mul_sched_1",
            "hourly_cooling_design_day": [0.8] * 24,
        },
        {
            "id": "lgt_mul_sche_1",
            "hourly_cooling_design_day": [0.6] * 24,
        },
        {
            "id": "misc_equip_schedule_1",
            "hourly_cooling_design_day": [0.3] * 24,
        },
    ],
    "type": "BASELINE_0",
}
TEST_RPD = {
    "id": "229_01",
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

TEST_RMD_UNIT = quantify_rmd(TEST_RPD)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_hvac_systems_primarily_serving_comp_room__hvac_1():

    assert get_hvac_systems_primarily_serving_comp_room(TEST_RMD_UNIT) == [
        "hvac_1"
    ]  # only hvac_1 meets the > 0.5 req
