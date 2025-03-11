from rct229.rulesets.ashrae9012019.ruleset_functions.is_economizer_modeled_in_proposed import (
    is_economizer_modeled_in_proposed,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD_FIXED_TYPE = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "floor_area": 100,
                                }
                            ],
                            "terminals": [
                                {
                                    "id": "Air Terminal",
                                    "is_supply_ducted": True,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 9",
                                }
                            ],
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 9",
                            "heating_system": {
                                "id": "Furnace Coil 1",
                                "type": "FURNACE",
                                "energy_source_type": "NATURAL_GAS",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 1",
                                "fan_control": "CONSTANT",
                                "supply_fans": [{"id": "Supply Fan 1"}],
                                "return_fans": [{"id": "Return Fan 1"}],
                                "air_economizer": {
                                    "id": "Air Economizer 1",
                                    "type": "FIXED_FRACTION",
                                },
                            },
                        }
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}

TEST_RMD_ENTHALPY_TYPE = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "floor_area": 100,
                                }
                            ],
                            "terminals": [
                                {
                                    "id": "Air Terminal",
                                    "is_supply_ducted": True,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 9",
                                }
                            ],
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 9",
                            "heating_system": {
                                "id": "Furnace Coil 1",
                                "type": "FURNACE",
                                "energy_source_type": "NATURAL_GAS",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 1",
                                "fan_control": "CONSTANT",
                                "supply_fans": [{"id": "Supply Fan 1"}],
                                "return_fans": [{"id": "Return Fan 1"}],
                                "air_economizer": {
                                    "id": "Air Economizer 1",
                                    "type": "ENTHALPY",  # enthalpy economizer type
                                },
                            },
                        }
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}

TEST_RMD_NO_ECONOMIZER_TYPE = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "floor_area": 100,
                                }
                            ],
                            "terminals": [
                                {
                                    "id": "Air Terminal",
                                    "is_supply_ducted": True,
                                    "type": "CONSTANT_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 9",
                                }
                            ],
                        }
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 9",
                            "heating_system": {
                                "id": "Furnace Coil 1",
                                "type": "FURNACE",
                                "energy_source_type": "NATURAL_GAS",
                            },
                            "fan_system": {
                                "id": "CAV Fan System 1",
                                "fan_control": "CONSTANT",
                                "supply_fans": [{"id": "Supply Fan 1"}],
                                "return_fans": [{"id": "Return Fan 1"}],
                                "air_economizer": {
                                    "id": "Air Economizer 1",  # No economizer type
                                },
                            },
                        }
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}


TEST_RPD_FIXED_TYPE = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD_FIXED_TYPE],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RPD_ENTHALPY_TYPE = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD_ENTHALPY_TYPE],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RPD_NO_ECONOMIZER_TYPE = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD_NO_ECONOMIZER_TYPE],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RMD_FIXED_TYPE_UNIT = quantify_rmd(TEST_RPD_FIXED_TYPE)[
    "ruleset_model_descriptions"
][0]

TEST_RMD_ENTHALPY_TYPE_UNIT = quantify_rmd(TEST_RPD_ENTHALPY_TYPE)[
    "ruleset_model_descriptions"
][0]

TEST_RMD_NO_ECONOMIZER_TYPE_UNIT = quantify_rmd(TEST_RPD_NO_ECONOMIZER_TYPE)[
    "ruleset_model_descriptions"
][0]


def test__BASELINE_TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FIXED_TYPE)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__PROPOSED_TEST_RPD_ENTHALPY_ECONOMIZER_TYPE__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_ENTHALPY_TYPE)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__PROPOSED_TEST_RPD_NO_ECONOMIZER_TYPE__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_NO_ECONOMIZER_TYPE)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_economizer_modeled_in_proposed_fixed_fraction_economizer_type():
    assert not is_economizer_modeled_in_proposed(
        TEST_RMD_FIXED_TYPE_UNIT, TEST_RMD_FIXED_TYPE_UNIT, "System 9"
    )


def test__is_economizer_modeled_in_proposed__enthalpy_economizer_type():
    assert is_economizer_modeled_in_proposed(
        TEST_RMD_FIXED_TYPE_UNIT, TEST_RMD_ENTHALPY_TYPE_UNIT, "System 9"
    )


def test__is_economizer_modeled_in_proposed__no_economizer_type():
    assert not is_economizer_modeled_in_proposed(
        TEST_RMD_FIXED_TYPE_UNIT, TEST_RMD_NO_ECONOMIZER_TYPE_UNIT, "System 9"
    )
