from rct229.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)

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
}


def test_get_hvac_zone_terminals():
    assert ordered(
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(TEST_RMD)
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
