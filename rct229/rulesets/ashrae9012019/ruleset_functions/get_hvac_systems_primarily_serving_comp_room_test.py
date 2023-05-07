from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_primarily_serving_comp_room import (
    get_hvac_systems_primarily_serving_comp_room,
)
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMI = {
    "id": "test_rmi",
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
                            "id": "zone_1_1",
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "spaces": [
                                {
                                    "id": "space_1_1_1",
                                    "floor_area": 1000,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                                {
                                    "id": "space_1_1_2",
                                    "floor_area": 500,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
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
                            "id": "zone_1_2",
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "spaces": [
                                {
                                    "id": "space_2_1_1",
                                    "floor_area": 1000,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                                {
                                    "id": "space_2_1_2",
                                    "floor_area": 500,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
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
}
TEST_RMD = {"id": "229_01", "ruleset_model_instances": [TEST_RMI]}

TEST_RMI_UNIT = quantify_rmr(TEST_RMD)["ruleset_model_instances"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_hvac_systems_primarily_serving_comp_room__hvac_1():
    # hvac_1 true, hvac_2 false
    assert get_hvac_systems_primarily_serving_comp_room(TEST_RMI_UNIT) == ["hvac_1"]
