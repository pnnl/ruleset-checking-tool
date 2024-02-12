import pytest

from rct229.rulesets.ashrae9012019.ruleset_functions.are_all_hvac_sys_fan_objects_autosized import (
    are_all_hvac_sys_fan_objs_autosized,
)
from rct229.schema.validate import schema_validate_rmr
from rct229.utils.assertions import MissingKeyException

TEST_RMI = {
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
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_4",
                                    "fan": {
                                        "id": "Terminal Fan 1",
                                        "is_airflow_sized_based_on_design_day": True,
                                    },
                                },
                                {
                                    "id": "terminal_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_5",
                                    "fan": {
                                        "id": "Terminal Fan 2",
                                        "is_airflow_sized_based_on_design_day": True,
                                    },
                                },
                                {
                                    "id": "terminal_3",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_5",
                                    "fan": {
                                        "id": "Terminal Fan 3",
                                        "is_airflow_sized_based_on_design_day": False,
                                    },
                                },
                                {
                                    "id": "terminal_4",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_6",
                                    "fan": {
                                        "id": "Terminal Fan 4",
                                        "is_airflow_sized_based_on_design_day": True,
                                    },
                                },
                                {
                                    "id": "terminal_5",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_6",
                                    "fan": {
                                        "id": "Terminal Fan 5",
                                    },
                                },
                            ],
                        },
                        {
                            "id": "zone_2",
                            "terminals": [
                                {
                                    # Failed outcome hvac_2 fan autosized is false.
                                    "id": "terminal_6",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2",
                                    "fan": {
                                        "id": "Terminal Fan 6",
                                        "is_airflow_sized_based_on_design_day": True,
                                    },
                                }
                            ],
                        },
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            # Success case - is_airflow_sized_based_on_design_day => True
                            "id": "hvac_1",
                            "fan_system": {
                                "id": "VAV Fan System 1",
                                "fan_control": "VARIABLE_SPEED_DRIVE",
                                "supply_fans": [
                                    {
                                        "id": "Supply Fan 1",
                                        "is_airflow_sized_based_on_design_day": True,
                                    }
                                ],
                            },
                        },
                        {
                            # Failed case - is_airflow_sized_based_on_design_day => False (at least one one)
                            "id": "hvac_2",
                            "fan_system": {
                                "id": "VAV Fan System 2",
                                "fan_control": "VARIABLE_SPEED_DRIVE",
                                "supply_fans": [
                                    {
                                        "id": "Supply Fan 2-1",
                                        "is_airflow_sized_based_on_design_day": True,
                                    },
                                    {
                                        "id": "Supply Fan 2-2",
                                        "is_airflow_sized_based_on_design_day": False,
                                    },
                                ],
                            },
                        },
                        {
                            # Raise exception case - is_airflow_sized_based_on_design_day => Missing
                            "id": "hvac_3",
                            "fan_system": {
                                "id": "VAV Fan System 3",
                                "fan_control": "VARIABLE_SPEED_DRIVE",
                                "supply_fans": [
                                    {
                                        "id": "Supply Fan 3-1",
                                        "is_airflow_sized_based_on_design_day": True,
                                    },
                                    {
                                        "id": "Supply Fan 3-2",
                                    },
                                ],
                            },
                        },
                        {
                            # Success case, all terminal fans are autosized
                            "id": "hvac_4",
                        },
                        {
                            # Failed case, one terminal fan is false
                            "id": "hvac_5",
                        },
                        {
                            # Raise Exception case, one terminal fan has no autosized data.
                            "id": "hvac_6",
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
    "ruleset_model_descriptions": [TEST_RMI],
    "data_timestamp": "2024-02-12T09:00Z",
}


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__hvac_fan_all_autosized__success():
    assert are_all_hvac_sys_fan_objs_autosized(TEST_RMI, "hvac_1") is True


def test__hvac_fan_partial_autosized__failed():
    assert are_all_hvac_sys_fan_objs_autosized(TEST_RMI, "hvac_2") is False


def test__hvac_fan_missing_autosized__exception():
    with pytest.raises(MissingKeyException):
        are_all_hvac_sys_fan_objs_autosized(TEST_RMI, "hvac_3")


def test_hvac_fan_all_terminal_autosized__success():
    assert are_all_hvac_sys_fan_objs_autosized(TEST_RMI, "hvac_4") is True


def test_hvac_fan_all_terminal_fan_partial_autosized__failed():
    assert are_all_hvac_sys_fan_objs_autosized(TEST_RMI, "hvac_5") is False


def test__hvac_terminal_fan_missing_autosized__exception():
    with pytest.raises(MissingKeyException):
        are_all_hvac_sys_fan_objs_autosized(TEST_RMI, "hvac_6")
