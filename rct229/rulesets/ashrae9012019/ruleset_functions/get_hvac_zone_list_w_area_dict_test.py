from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMR = {
    "id": "test_rmr",
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                {
                    "id": "bldg_seg_1",
                    "heating_ventilating_air_conditioning_systems": [
                        {"id": "hvac_1_1"}
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
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_1",
                                },
                                {
                                    "id": "terminal_1_1_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_1",
                                },
                            ],
                        },
                        {
                            "id": "zone_1_2",
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}
TEST_RMR_12 = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMR],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_BUILDING = quantify_rmr(TEST_RMR_12)["ruleset_model_descriptions"][0]["buildings"][
    0
]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMR_12)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_hvac_zone_list_w_area_dict():
    assert get_hvac_zone_list_w_area_dict(TEST_BUILDING) == {
        "hvac_1_1": {"zone_list": ["zone_1_1"], "total_area": 1500 * ureg.m2}
    }
