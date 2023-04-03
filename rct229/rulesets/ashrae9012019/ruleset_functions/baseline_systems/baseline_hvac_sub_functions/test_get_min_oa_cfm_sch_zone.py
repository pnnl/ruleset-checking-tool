from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.get_min_oa_cfm_sch_zone import (
    get_min_oa_cfm_sch_zone,
)
from rct229.schema.validate import schema_validate_rmr

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "zones": [
                        {
                            "id": "Zone 1",
                            "terminals": [
                                {
                                    "id": "Terminal 1",
                                    "minimum_outdoor_airflow": 10,
                                    "minimum_outdoor_airflow_multiplier_schedule": "Schedule 1",
                                },
                                {
                                    "id": "Terminal 2",
                                    "minimum_outdoor_airflow": 10,
                                    "minimum_outdoor_airflow_multiplier_schedule": "Schedule 2",
                                },
                            ],
                        },
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "hvac_1",
                            "preheat_system": {
                                "id": "preheat_system",
                                "hot_water_loop": "HW_Loop_1",
                                "heating_system_type": "FLUID_LOOP",
                            },
                        }
                    ],
                }
            ],
        }
    ],
    "schedules": [
        {
            "id": "Schedule 1",
            "hourly_values": [0.3] * 8760,
        },
        {
            "id": "Schedule 2",
            "hourly_values": [0.4] * 8760,
        },
    ],
    "boilers": [
        {
            "id": "boiler_1",
            "loop": "HW_Loop_1",
        }
    ],
    "fluid_loops": [
        {
            "id": "HW_Loop_1",
            "type": "HEATING",
        }
    ],
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_min_oa_cfm_sch_zone__pass():
    assert get_min_oa_cfm_sch_zone(TEST_RMD, "Zone 1") == [7.0] * 8760
