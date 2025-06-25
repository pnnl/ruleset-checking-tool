import pytest
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_BPF_BAT import (
    get_zone_BPF_BAT,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd
from rct229.utils.assertions import RCTFailureException

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
                        {
                            "id": "zone_3",
                            "spaces": [
                                # to test missing `lighting_space_type` key
                                {
                                    "id": "Space 3_1",
                                }
                            ],
                        },
                        {
                            "id": "zone_4",
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
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RMD = quantify_rmd(TEST_RPD)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_zone_BPF_BAT__all_undetermined():
    assert get_zone_BPF_BAT(TEST_RMD, "zone_1") == {"UNDETERMINED": 300 * ureg("m2")}


def test__get_zone_BPF_BAT__all_diff_bldg_type():
    assert get_zone_BPF_BAT(TEST_RMD, "zone_2") == {
        "HEALTHCARE_HOSPITAL": 700 * ureg("m2"),
        "ALL_OTHER": 100 * ureg("m2"),
    }


def test__get_zone_BPF_BAT__no_lgt_type():
    assert get_zone_BPF_BAT(TEST_RMD, "zone_3") == {"UNDETERMINED": 0 * ureg("m2")}


def test__get_zone_BPF_BAT__no_spaces():
    with pytest.raises(
        RCTFailureException,
        match="No spaces have been found in zone `zone_4`. Check the RPD inputs.",
    ):
        get_zone_BPF_BAT(TEST_RMD, "zone_4")
