from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_serving_zone_health_safety_vent_reqs import (
    get_hvac_systems_serving_zone_health_safety_vent_reqs,
)
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMI = {
    "id": "test_rmi",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "zones": [
                        # case 1 - lighting_space_type => system 1, system 2
                        {
                            "id": "zone 1",
                            "spaces": [
                                {
                                    "id": "space_1",
                                    "lighting_space_type": "MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA",
                                },
                                {
                                    "id": "space_2",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                                {
                                    "id": "terminal_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                                {
                                    "id": "terminal_3",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                            ],
                        },
                        # case 2 - ventilation_space_type => system 3
                        {
                            "id": "zone 2",
                            "spaces": [
                                {
                                    "id": "space_3",
                                    "ventilation_space_type": "ANIMAL_FACILITIES_ANIMAL_IMAGING_MRI_CT_PET",
                                },
                                {
                                    "id": "space_4",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_4",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 3",
                                },
                            ],
                        },
                        # Case 3 - no match
                        {
                            "id": "zone 3",
                            "spaces": [
                                {
                                    "id": "space_5",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_5",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 4",
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

TEST_RMD = quantify_rmr(
    {
        "id": "229_01",
        "ruleset_model_descriptions": [TEST_RMI],
        "data_timestamp": "2024-02-12T09:00Z",
    }
)
TEST_RMI_UNIT = TEST_RMD["ruleset_model_descriptions"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_hvac_systems_serving_zone_health_safety_vent_reqs__success():
    assert sorted(
        get_hvac_systems_serving_zone_health_safety_vent_reqs(TEST_RMI_UNIT)
    ) == ["System 1", "System 2", "System 3"]
