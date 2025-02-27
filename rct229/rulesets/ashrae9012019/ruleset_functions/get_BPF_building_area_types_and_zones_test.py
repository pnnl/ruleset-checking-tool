from rct229.rulesets.ashrae9012019.ruleset_functions.get_BPF_building_area_types_and_zones import (
    get_BPF_building_area_types_and_zones,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_BUILDING_WITH_LGT_BAT = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "lighting_building_area_type": "CONVENTION_CENTER",
                    "heating_ventilating_air_conditioning_systems": [
                        {"id": "hvac_1"},
                    ],
                    "zones": [
                        {
                            "id": "zone_1",
                            "spaces": [
                                {
                                    "id": "Space 1_1",
                                    "floor_area": 100,
                                },
                                {
                                    "id": "Space 1_2",
                                    "floor_area": 200,
                                },
                            ],
                        },
                        {
                            "id": "zone_2",
                            "spaces": [
                                {
                                    "id": "Space 2_1",
                                    "floor_area": 300,
                                },
                                {
                                    "id": "Space 2_2",
                                    "floor_area": 400,
                                },
                                {
                                    "id": "Space 2_3",
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

TEST_BUILDING_WITHOUT_LGT_BAT = {
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


TEST_RPD_WITH_LGT_BAT = {
    "id": "ASHRAE229",
    "ruleset_model_descriptions": [TEST_BUILDING_WITH_LGT_BAT],
}

TEST_RPD_WITHOUT_LGT_BAT = {
    "id": "ASHRAE229",
    "ruleset_model_descriptions": [TEST_BUILDING_WITHOUT_LGT_BAT],
}


TEST_RMD_WITH_LGT_BAT = quantify_rmd(TEST_RPD_WITH_LGT_BAT)[
    "ruleset_model_descriptions"
][0]
TEST_RMD_WITHOUT_LGT_BAT = quantify_rmd(TEST_RPD_WITHOUT_LGT_BAT)[
    "ruleset_model_descriptions"
][0]


def test__TEST_WITH_LGT_BAT__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_WITH_LGT_BAT)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_WITHOUT_LGT_BAT__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_WITHOUT_LGT_BAT)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_BPF_building_area_types_and_zones__With_lgt_bat():
    assert get_BPF_building_area_types_and_zones(TEST_RMD_WITH_LGT_BAT) == {
        "ALL_OTHER": {
            "zone_id": ["zone_1", "zone_2"],
            "area": 1100 * ureg("m2"),
            "classification_source": "BUILDING_SEGMENT_LIGHTING",
        }
    }


def test__get_BPF_building_area_types_and_zones__Without_lgt_bat():
    assert get_BPF_building_area_types_and_zones(TEST_RMD_WITHOUT_LGT_BAT) == {
        "UNDETERMINED": {
            "zone_id": ["zone_1"],
            "area": 300 * ureg("m2"),
            "classification_source": "SPACE_LIGHTING",
        },
        "HEALTHCARE_HOSPITAL": {
            "zone_id": ["zone_2"],
            "area": 800 * ureg("m2"),
            "classification_source": "SPACE_LIGHTING",
        },
    }
