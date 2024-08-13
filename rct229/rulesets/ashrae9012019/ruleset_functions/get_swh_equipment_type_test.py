from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_type import (
    get_swh_equipment_type,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rmd


TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                }
            ],
        }
    ],
    "service_water_heating_equipment": [
        {
            "id": "swh equipment 1",
            "distribution_system": "distribution system 1",
            "tank": [
                {"id": "Tank 1", "type": "CONSUMER_INSTANTANEOUS"},
                {"id": "Tank 2", "type": "CONSUMER_STORAGE"},
            ],
            "heater_type": "HEAT_FROM_HOT_WATER_LOOP",
            "heater_fuel_type": "ELECTRICITY",
        }
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rmd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_swh_equipment_type__electric_instantaneous():
    assert (
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 1",
        )
        == "ELECTRIC_RESISTANCE_INSTANTANEOUS"
    )
