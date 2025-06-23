import pytest
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_type import (
    GetSWHEquipmentType,
    get_swh_equipment_type,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd
from rct229.utils.assertions import RCTFailureException

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
            "tank": {"id": "Tank 1", "type": "CONSUMER_INSTANTANEOUS"},
            "heater_fuel_type": "ELECTRICITY",
        },
        {
            "id": "swh equipment 2",
            "distribution_system": "distribution system 2",
            "tank": {"id": "Tank 2", "type": "CONSUMER_INSTANTANEOUS"},
            "heater_fuel_type": "NATURAL_GAS",
        },
        {
            "id": "swh equipment 3",
            "distribution_system": "distribution system 3",
            "tank": {"id": "Tank 3", "type": "COMMERCIAL_INSTANTANEOUS"},
            "heater_fuel_type": "FUEL_OIL",
        },
        {
            "id": "swh equipment 4",
            "distribution_system": "distribution system 4",
            "tank": {"id": "Tank 4", "type": "CONSUMER_STORAGE"},
            "heater_fuel_type": "ELECTRICITY",
        },
        {
            "id": "swh equipment 5",
            "distribution_system": "distribution system 5",
            "tank": {"id": "Tank 5", "type": "CONSUMER_STORAGE"},
            "heater_fuel_type": "NATURAL_GAS",
        },
        {
            "id": "swh equipment 6",
            "distribution_system": "distribution system 6",
            "tank": {"id": "Tank 6", "type": "COMMERCIAL_STORAGE"},
            "heater_fuel_type": "FUEL_OIL",
        },
        {
            "id": "swh equipment 7",
            "distribution_system": "distribution system 7",
            "tank": {"id": "Tank 7", "type": "OTHER"},
            "compressor_heat_rejection_source": "CONDITIONED",
            "heater_fuel_type": "ELECTRICITY",
        },
        {
            "id": "swh equipment 8",
            "distribution_system": "distribution system 8",
            "tank": {"id": "Tank 8", "type": "CONSUMER_STORAGE"},
            "heater_fuel_type": "PROPANE",
        },
        {
            "id": "swh equipment 9",
            "distribution_system": "distribution system 9",
            "tank": {"id": "Tank 9", "type": "OTHER"},
            "compressor_power_operating_points": [{"evaporator_air_temperature": 23}],
            "heater_fuel_type": "OTHER",
        },
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_swh_equipment_type__electric_instantaneous():
    assert (
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 1",
        )
        == GetSWHEquipmentType.ELECTRIC_RESISTANCE_INSTANTANEOUS
    )


def test__get_swh_equipment_type__gas_instantaneous():
    assert (
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 2",
        )
        == GetSWHEquipmentType.GAS_INSTANTANEOUS
    )


def test__get_swh_equipment_type__oil_instantaneous():
    assert (
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 3",
        )
        == GetSWHEquipmentType.OIL_INSTANTANEOUS
    )


def test__get_swh_equipment_type__electric_storage():
    assert (
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 4",
        )
        == GetSWHEquipmentType.ELECTRIC_RESISTANCE_STORAGE
    )


def test__get_swh_equipment_type__gas_storage():
    assert (
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 5",
        )
        == GetSWHEquipmentType.GAS_STORAGE
    )


def test__get_swh_equipment_type__oil_storage():
    assert (
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 6",
        )
        == GetSWHEquipmentType.OIL_STORAGE
    )


def test__get_swh_equipment_type__other():
    assert (
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 7",
        )
        == GetSWHEquipmentType.OTHER
    )


def test__get_swh_equipment_type__propane_storage():
    assert (
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 8",
        )
        == GetSWHEquipmentType.PROPANE_STORAGE
    )


def test__get_swh_equipment_type__wrong_fuel_type():
    with pytest.raises(
        RCTFailureException,
        match="Fuel type must be one of `ELECTRICITY`, `NATURAL_GAS`, `PROPANE`, `FUEL_OIL`.",
    ):
        get_swh_equipment_type(
            TEST_RMD,
            "swh equipment 9",
        )
