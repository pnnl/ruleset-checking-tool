from rct229.rulesets.ashrae9012019.ruleset_functions.get_fuels_modeled_in_rmd import (
    get_fuels_modeled_in_rmd,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RPD_NG_ELEC = {
    "id": "ASHRAE229 1",
    "ruleset_model_descriptions": [
        {
            "id": "RMD 1",
            "buildings": [
                {
                    "id": "Building 1",
                    "building_segments": [
                        {
                            "id": "Building Segment 1",
                            "zones": [
                                {
                                    "id": "Thermal Zone 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1",
                                            "heating_source": "HOT_WATER",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 7",
                                    "heating_system": {
                                        "id": "Heating Coil 1",
                                        "energy_source_type": "NATURAL_GAS",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "energy_source_type": "NATURAL_GAS",
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "boilers": [
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "energy_source_type": "NATURAL_GAS",
                }
            ],
            "chillers": [
                {
                    "id": "Chiller 1",
                    "cooling_loop": "Chiller Loop 1",
                    "condensing_loop": "Condensing Loop 1",
                    "energy_source_type": "ELECTRICITY",
                },
            ],
            "service_water_heating_equipment": [
                {
                    "id": "SWH equip 1",
                    "distribution_system": "SWH dist system 1",
                    "heater_fuel_type": "NATURAL_GAS",
                }
            ],
            "type": "BASELINE_0",
        }
    ],
}


TEST_RPD_PROPANE_NG_ELEC = {
    "id": "ASHRAE229 1",
    "ruleset_model_descriptions": [
        {
            "id": "RMD 1",
            "buildings": [
                {
                    "id": "Building 1",
                    "building_segments": [
                        {
                            "id": "Building Segment 1",
                            "zones": [
                                {
                                    "id": "Thermal Zone 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1",
                                            "heating_source": "HOT_WATER",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 7",
                                    "heating_system": {
                                        "id": "Heating Coil 1",
                                        "energy_source_type": "NATURAL_GAS",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "energy_source_type": "NATURAL_GAS",
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "boilers": [
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "energy_source_type": "PROPANE",
                }
            ],
            "chillers": [
                {
                    "id": "Chiller 1",
                    "cooling_loop": "Chiller Loop 1",
                    "condensing_loop": "Condensing Loop 1",
                    "energy_source_type": "ELECTRICITY",
                },
            ],
            "service_water_heating_equipment": [
                {
                    "id": "SWH equip 1",
                    "distribution_system": "SWH dist system 1",
                    "heater_fuel_type": "NATURAL_GAS",
                }
            ],
            "type": "BASELINE_0",
        }
    ],
}


TEST_RPD_ALL_ENERGY_SOURCE = {
    "id": "ASHRAE229 1",
    "ruleset_model_descriptions": [
        {
            "id": "RMD 1",
            "buildings": [
                {
                    "id": "Building 1",
                    "building_segments": [
                        {
                            "id": "Building Segment 1",
                            "zones": [
                                {
                                    "id": "Thermal Zone 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1",
                                            "heating_source": "HOT_WATER",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 7",
                                    "heating_system": {
                                        "id": "Heating Coil 1",
                                        "energy_source_type": "FUEL_OIL",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "energy_source_type": "OTHER",
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "boilers": [
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "energy_source_type": "PROPANE",
                }
            ],
            "chillers": [
                {
                    "id": "Chiller 1",
                    "cooling_loop": "Chiller Loop 1",
                    "condensing_loop": "Condensing Loop 1",
                    "energy_source_type": "ELECTRICITY",
                },
            ],
            "external_fluid_sources": [
                {
                    "id": "Ext Fluid Source 1",
                    "loop": "Ext loop 1",
                    "energy_source_type": "ELECTRICITY",
                }
            ],
            "service_water_heating_equipment": [
                {
                    "id": "SWH equip 1",
                    "distribution_system": "SWH dist system 1",
                    "heater_fuel_type": "NATURAL_GAS",
                }
            ],
            "type": "BASELINE_0",
        }
    ],
}


TEST_RMD_NG_ELEC = quantify_rmd(TEST_RPD_NG_ELEC)["ruleset_model_descriptions"][0]
TEST_RMD_PROPANE_NG_ELEC = quantify_rmd(TEST_RPD_PROPANE_NG_ELEC)[
    "ruleset_model_descriptions"
][0]
TEST_RMD_ALL_ENERGY_SOURCE = quantify_rmd(TEST_RPD_ALL_ENERGY_SOURCE)[
    "ruleset_model_descriptions"
][0]


def test__TEST_RPD_NG_ELEC__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_NG_ELEC)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RPD_PROPANE_NG_ELEC__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_PROPANE_NG_ELEC)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_all_energy_source__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_ALL_ENERGY_SOURCE)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_fuels_modeled_in_rmd__natural_gas_elec():
    fuels_list = get_fuels_modeled_in_rmd(TEST_RMD_NG_ELEC)
    assert fuels_list == ["NATURAL_GAS", "ELECTRICITY"]


def test__get_fuels_modeled_in_rmd__propane_natural_gas_elec():
    fuels_list = get_fuels_modeled_in_rmd(TEST_RMD_PROPANE_NG_ELEC)
    assert fuels_list == ["PROPANE", "NATURAL_GAS", "ELECTRICITY"]


def test__get_fuels_modeled_in_rmd__all_energy_source():
    fuels_list = get_fuels_modeled_in_rmd(TEST_RMD_ALL_ENERGY_SOURCE)
    assert fuels_list == ["PROPANE", "NATURAL_GAS", "ELECTRICITY", "OIL", "OTHER"]
