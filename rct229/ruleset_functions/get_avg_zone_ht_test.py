import pytest

from rct229.ruleset_functions.get_avg_zone_ht import get_avg_zone_ht
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

# Constants
M = ureg("meters")
M3 = ureg("meters ** 3")

TEST_RMR = {
    "id": "229_01",
    "ruleset_model_instances": [
        {
            "id": "test_rmr",
            "buildings": [
                {
                    "id": "bldg_1",
                    "building_open_schedule": "bldg_open_sched_1",
                    "building_segments": [
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
                                            "floor_area": 10,  # m2
                                            "occupant_multiplier_schedule": "occ_mult_sched_1",
                                        }
                                    ],
                                    "volume": 100,  # m3
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    ],
}


TEST_ZONE = quantify_rmr(TEST_RMR)["ruleset_model_instances"][0]["buildings"][0][
    "building_segments"
][0]["zones"][0]


def test__TEST_RMR__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMR)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_avg_zone_ht():
    assert get_avg_zone_ht(TEST_ZONE) == 10 * M
