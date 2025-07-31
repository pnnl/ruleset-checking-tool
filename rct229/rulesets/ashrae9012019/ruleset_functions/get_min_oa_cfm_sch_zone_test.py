import pytest
from rct229.rulesets.ashrae9012019.ruleset_functions.get_min_oa_cfm_sch_zone import (
    get_min_oa_cfm_sch_zone,
)
from rct229.schema.validate import schema_validate_rpd
from rct229.utils.assertions import RCTFailureException


def create_flexible_schedule_length(schedule_length):
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
                                    "type": "FLUID_LOOP",
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
                "hourly_values": [0.3] * schedule_length,
            },
            {
                "id": "Schedule 2",
                "hourly_values": [0.4] * schedule_length,
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
        "type": "BASELINE_0",
    }
    return TEST_RMD


TEST_RMD_CORRECT_LENGTH = create_flexible_schedule_length(8760)
TEST_RMD_WRONG_LENGTH = create_flexible_schedule_length(8700)

TEST_RPD_FULL_CORRECT_LENGTH = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD_CORRECT_LENGTH],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}
TEST_RPD_FULL_WRONG_LENGTH = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD_WRONG_LENGTH],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}


def test__TEST_RMD_CORRECT_LENGTH__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL_CORRECT_LENGTH)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_WRONG_LENGTH__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL_WRONG_LENGTH)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_min_oa_cfm_sch_zone__pass():
    assert get_min_oa_cfm_sch_zone(TEST_RMD_CORRECT_LENGTH, "Zone 1") == [7.0] * 8760
