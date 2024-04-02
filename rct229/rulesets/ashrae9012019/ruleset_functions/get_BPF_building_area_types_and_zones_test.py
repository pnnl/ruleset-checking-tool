from rct229.rulesets.ashrae9012019.ruleset_functions.get_BPF_building_area_types_and_zones import (
    get_BPF_building_area_types_and_zones,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr


TEST_BUILDING = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "heating_ventilating_air_conditioning_systems": [
                        {"id": "hvac_1"},
                    ],
                    "zones": [
                        {
                            "id": "zone_1",
                            "spaces": [
                                # sll the lighting_space_type fall into `UNDETERMINED`
                                {
                                    "id": "Space 1_1",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                    "floor_area": 100,
                                },
                                {
                                    "id": "Space 1_2",
                                    "lighting_space_type": "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER",
                                    "floor_area": 200,
                                },
                            ],
                        },
                        {
                            "id": "zone_2",
                            "spaces": [
                                # lighting_space_type fallS into `HEALTHCARE_HOSPITAL` AND `ALL_OTHER`
                                {
                                    "id": "Space 2_1",
                                    "lighting_space_type": "HEALTHCARE_FACILITY_NURSES_STATION",
                                    "floor_area": 300,
                                },
                                {
                                    "id": "Space 2_2",
                                    "lighting_space_type": "HEALTHCARE_FACILITY_PATIENT_ROOM",
                                    "floor_area": 400,
                                },
                                {
                                    "id": "Space 2_3",
                                    "lighting_space_type": "MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA",
                                    "floor_area": 100,
                                },
                            ],
                        },
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}


TEST_RPD = {
    "id": "ASHRAE229",
    "ruleset_model_descriptions": [TEST_BUILDING],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD = quantify_rmr(TEST_RPD)["ruleset_model_descriptions"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RPD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_BPF_building_area_types_and_zones__pass():
    assert get_BPF_building_area_types_and_zones(TEST_RMD) == {
        "HEALTHCARE_HOSPITAL": {
            "zone_id": ["zone_1", "zone_2"],
            "area": 1100 * ureg("m2"),
            "classification_source": "SPACE_LIGHTING",
        }
    }
