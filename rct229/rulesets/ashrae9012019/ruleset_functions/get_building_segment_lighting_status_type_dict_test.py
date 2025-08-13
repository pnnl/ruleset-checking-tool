from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_lighting_status_type_dict import (
    LightingStatusType as LST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_lighting_status_type_dict import (
    get_building_segment_lighting_status_type_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

# Convert LPD value to schema units
FIRE_STATION_ALLOWED_LPD = (0.56 * ureg("W/(foot**2)")).to("W/(m**2)").magnitude

TEST_RMD = {
    "id": "229_01",
    "ruleset_model_descriptions": [
        {
            "id": "test_rmd",
            "buildings": [
                {
                    "id": "bldg_1",
                    "building_open_schedule": "bldg_open_sched_1",
                    "building_segments": [
                        # Case: Missing lighting_building_area_type
                        {
                            "id": "bldg_seg_1",
                            "zones": [
                                {
                                    "id": "zone_1_1",
                                    "thermostat_cooling_setpoint_schedule": "therm_cooling_setpoint_sched_1",
                                    "thermostat_heating_setpoint_schedule": "therm_heating_setpoint_sched_1",
                                    "spaces": [
                                        {
                                            "id": "space_1_1_1",
                                            "occupant_multiplier_schedule": "occ_mult_sched_1",
                                        }
                                    ],
                                },
                            ],
                        },
                        # Case: lighting_building_area_type == "NONE"
                        {
                            "id": "bldg_seg_2",
                            "lighting_building_area_type": "NONE",
                            "zones": [
                                {
                                    "id": "zone_2_1",
                                    "thermostat_cooling_setpoint_schedule": "therm_cooling_setpoint_sched_1",
                                    "thermostat_heating_setpoint_schedule": "therm_heating_setpoint_sched_1",
                                    "spaces": [
                                        {
                                            "id": "space_2_1_1",
                                            "occupant_multiplier_schedule": "occ_mult_sched_1",
                                        }
                                    ],
                                },
                            ],
                        },
                        # Case lighting_building_area_type in not "NONE"
                        # FIRE_STATION => allowable_lpd = 0.56 w/ft^2
                        {
                            "id": "bldg_seg_3",
                            "lighting_building_area_type": "FIRE_STATION",
                            "zones": [
                                {
                                    "id": "zone_3_1",
                                    "thermostat_cooling_setpoint_schedule": "therm_cooling_setpoint_sched_1",
                                    "thermostat_heating_setpoint_schedule": "therm_heating_setpoint_sched_1",
                                    "spaces": [
                                        # Power per area matches allowed lpd
                                        {
                                            "id": "space_3_1_1",
                                            "interior_lighting": [
                                                {
                                                    "id": "int_lighting_3_1_1_1",
                                                    "lighting_multiplier_schedule": "lighting_mult_sched_1",
                                                    "power_per_area": FIRE_STATION_ALLOWED_LPD,
                                                }
                                            ],
                                            "occupant_multiplier_schedule": "occ_mult_sched_1",
                                        },
                                        # Power per area does not match allowed lpd
                                        {
                                            "id": "space_3_1_2",
                                            "interior_lighting": [
                                                {
                                                    "id": "int_lighting_3_1_2_1",
                                                    "lighting_multiplier_schedule": "lighting_mult_sched_1",
                                                    "power_per_area": FIRE_STATION_ALLOWED_LPD
                                                    / 2,
                                                }
                                            ],
                                            "occupant_multiplier_schedule": "occ_mult_sched_1",
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                }
            ],
            "type": "BASELINE_0",
        }
    ],
}

TEST_BUILDING = quantify_rmd(TEST_RMD)["ruleset_model_descriptions"][0]["buildings"][0]
test_building_segments = TEST_BUILDING["building_segments"]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_building_segment_lighting_status_type_dict__building_segment_1():
    assert get_building_segment_lighting_status_type_dict(
        test_building_segments[0]
    ) == {"space_1_1_1": LST.AS_DESIGNED_OR_AS_EXISTING}


def test__get_building_segment_lighting_status_type_dict__building_segment_2():
    assert get_building_segment_lighting_status_type_dict(
        test_building_segments[1]
    ) == {"space_2_1_1": LST.AS_DESIGNED_OR_AS_EXISTING}


def test__get_building_segment_lighting_status_type_dict__building_segment_3():
    assert get_building_segment_lighting_status_type_dict(
        test_building_segments[2]
    ) == {
        "space_3_1_1": LST.NOT_YET_DESIGNED_OR_MATCH_TABLE_9_5_1,
        "space_3_1_2": LST.AS_DESIGNED_OR_AS_EXISTING,
    }
