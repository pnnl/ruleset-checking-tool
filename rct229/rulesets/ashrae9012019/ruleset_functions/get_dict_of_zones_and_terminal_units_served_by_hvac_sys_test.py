from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.schema.validate import schema_validate_rpd

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
                        {"id": "hvac_2"},
                        {"id": "hvac_3"},
                        {"id": "hvac_4"},
                    ],
                    "zones": [
                        {
                            "id": "zone_1",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1",
                                },
                                {
                                    "id": "terminal_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2",
                                },
                                {
                                    "id": "terminal_3",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_3",
                                },
                                {
                                    "id": "terminal_4",
                                    # intentionally omit `served_by_heating_ventilating_air_conditioning_system` key to test 'if hvac_sys_id:' condition in get_dict_of_zones_and_terminal_units_served_by_hvac_sys.py
                                },
                                {
                                    # intentionally added the duplicate to test 'if terminal_id not in terminal_unit_list:' condition in get_dict_of_zones_and_terminal_units_served_by_hvac_sys.py
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1",
                                },
                            ],
                        },
                        {
                            "id": "zone_2",
                            "terminals": [
                                {
                                    "id": "terminal_4",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_4",
                                },
                                {
                                    "id": "terminal_5",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2",
                                },
                                {
                                    "id": "terminal_6",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_4",
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


TEST_RMD = {
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


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_get_hvac_zone_terminals():
    assert ordered(
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(TEST_BUILDING)
    ) == ordered(
        {
            "hvac_1": {"terminal_unit_list": ["terminal_1"], "zone_list": ["zone_1"]},
            "hvac_2": {
                "terminal_unit_list": ["terminal_2", "terminal_5"],
                "zone_list": ["zone_1", "zone_2"],
            },
            "hvac_3": {"terminal_unit_list": ["terminal_3"], "zone_list": ["zone_1"]},
            "hvac_4": {
                "terminal_unit_list": ["terminal_4", "terminal_6"],
                "zone_list": ["zone_2"],
            },
        }
    )


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
