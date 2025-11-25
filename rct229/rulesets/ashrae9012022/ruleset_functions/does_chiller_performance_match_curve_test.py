import copy

import pytest
from rct229.rulesets.ashrae9012022.ruleset_functions.does_chiller_performance_match_curve import (
    does_chiller_performance_match_curve,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd
from rct229.utils.assertions import RCTFailureException

TEST_RMD = {
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
                                    "is_supply_ducted": True,
                                    "type": "VARIABLE_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                    "heating_source": "HOT_WATER",
                                    "heating_from_loop": "Boiler Loop 1",
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "terminals": [
                                {
                                    "id": "VAV Air Terminal 2",
                                    "is_supply_ducted": True,
                                    "type": "VARIABLE_AIR_VOLUME",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                    "heating_source": "HOT_WATER",
                                    "heating_from_loop": "Boiler Loop 1",
                                }
                            ],
                        },
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 7",
                            "cooling_system": {
                                "id": "CHW Coil 1",
                                "type": "FLUID_LOOP",
                                "chilled_water_loop": "Secondary CHW Loop 1",
                            },
                            "preheat_system": {
                                "id": "Preheat Coil 1",
                                "type": "FLUID_LOOP",
                                "hot_water_loop": "Boiler Loop 1",
                            },
                            "fan_system": {
                                "id": "VAV Fan System 1",
                                "fan_control": "VARIABLE_SPEED_DRIVE",
                                "supply_fans": [{"id": "Supply Fan 1"}],
                                "return_fans": [{"id": "Return Fan 1"}],
                            },
                        }
                    ],
                }
            ],
        }
    ],
    "boilers": [
        {"id": "Boiler 1", "loop": "Boiler Loop 1", "energy_source_type": "NATURAL_GAS"}
    ],
    "chillers": [
        {
            "id": "Chiller 1",
            "cooling_loop": "Chiller Loop 1",
            "compressor_type": "CENTRIFUGAL",
            "rated_capacity": 527550.0,
            "condensing_loop": "Condenser Loop 1",
            "efficiency_metric_values": [5.5],
            "efficiency_metric_types": ["FULL_LOAD_EFFICIENCY_RATED"],
            "capacity_operating_points": [
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (60 * ureg("degF")).to("degC").m,
                    "capacity": 522221.2,
                },
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (104 * ureg("degF")).to("degC").m,
                    "capacity": 417000.3,
                },
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (85 * ureg("degF")).to("degC").m,
                    "capacity": 474715.3,
                },
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (72.5 * ureg("degF")).to("degC").m,
                    "capacity": 502507.3,
                },
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (97.5 * ureg("degF")).to("degC").m,
                    "capacity": 438845.2,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (60 * ureg("degF")).to("degC").m,
                    "capacity": 565443.4,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (104 * ureg("degF")).to("degC").m,
                    "capacity": 488077.1,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (85 * ureg("degF")).to("degC").m,
                    "capacity": 533764.0,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (72.5 * ureg("degF")).to("degC").m,
                    "capacity": 553642.8,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (97.5 * ureg("degF")).to("degC").m,
                    "capacity": 505807.2,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (60 * ureg("degF")).to("degC").m,
                    "capacity": 584604.0,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (104 * ureg("degF")).to("degC").m,
                    "capacity": 530449.9,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (85 * ureg("degF")).to("degC").m,
                    "capacity": 566113.4,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (72.5 * ureg("degF")).to("degC").m,
                    "capacity": 579397.7,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (97.5 * ureg("degF")).to("degC").m,
                    "capacity": 544750.9,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (60 * ureg("degF")).to("degC").m,
                    "capacity": 588439.3,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (104 * ureg("degF")).to("degC").m,
                    "capacity": 557497.4,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (85 * ureg("degF")).to("degC").m,
                    "capacity": 583137.4,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (72.5 * ureg("degF")).to("degC").m,
                    "capacity": 589827.4,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (97.5 * ureg("degF")).to("degC").m,
                    "capacity": 568369.3,
                },
            ],
            "power_operating_points": [
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (60 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 79979.2,
                },
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (72.5 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 93409.8,
                },
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (85.0 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 102356.5,
                },
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (97.5 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 107134.4,
                },
                {
                    "chilled_water_supply_temperature": (39 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (104 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 108084.6,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (60 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 71797.9,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (72.5 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 84935.4,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (85.0 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 93202.5,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (97.5 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 96760.4,
                },
                {
                    "chilled_water_supply_temperature": (45 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (104 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 96800.8,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (60 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 66960.6,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (72.5 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 80260.3,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (85.0 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 88538.4,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (97.5 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 91899.9,
                },
                {
                    "chilled_water_supply_temperature": (50 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (104 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 91737.6,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (60 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 63538.7,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (72.5 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 77160.5,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (85.0 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 85681.6,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (97.5 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 89177.3,
                },
                {
                    "chilled_water_supply_temperature": (55 * ureg("degF"))
                    .to("degC")
                    .m,
                    "condenser_temperature": (104 * ureg("degF")).to("degC").m,
                    "load": 522221.2,
                    "power": 89031.4,
                },
            ],
        }
    ],
    "pumps": [
        {
            "id": "Boiler Pump 1",
            "loop_or_piping": "Boiler Loop 1",
            "speed_control": "FIXED_SPEED",
        },
        {
            "id": "Chiller Pump 1",
            "loop_or_piping": "Chiller Loop 1",
            "speed_control": "FIXED_SPEED",
        },
        {
            "id": "Secondary CHW Pump",
            "loop_or_piping": "Secondary CHW Loop 1",
            "speed_control": "VARIABLE_SPEED",
        },
    ],
    "fluid_loops": [
        {"id": "Boiler Loop 1", "type": "HEATING"},
        {
            "id": "Chiller Loop 1",
            "type": "COOLING",
            "child_loops": [{"id": "Secondary CHW Loop 1", "type": "COOLING"}],
        },
        {"id": "Condenser Loop 1", "type": "CONDENSER"},
    ],
    "heat_rejections": [{"id": "Heat Rejection 1", "loop": "Condenser Loop 1"}],
    "type": "BASELINE_0",
}

TEST_RMD_12 = {
    "id": "229_01",
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

TEST_CHILLER = quantify_rmd(TEST_RMD_12)["ruleset_model_descriptions"][0]["chillers"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_12)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__does_chiller_performance_match_curve6__pass():
    assert does_chiller_performance_match_curve(TEST_CHILLER, "AA")


def test__does_chiller_performance_match_curve__full_load_efficiency_rated_not_exist():
    with pytest.raises(
        RCTFailureException,
        match="The `FULL_LOAD_EFFICIENCY_RATED` must exist in the `efficiency_metric_types`.",
    ):
        TEST_CHILLER_ZERO_EFFI = copy.deepcopy(TEST_CHILLER)
        TEST_CHILLER_ZERO_EFFI["efficiency_metric_types"] = []
        does_chiller_performance_match_curve(TEST_CHILLER_ZERO_EFFI, "AA")


def test__does_chiller_performance_match_curve__zero_full_load_efficiency_rated():
    with pytest.raises(
        RCTFailureException,
        match="The `efficiency_metric_values` must be greater than 0.",
    ):
        TEST_CHILLER_ZERO_EFFI = copy.deepcopy(TEST_CHILLER)
        TEST_CHILLER_ZERO_EFFI["efficiency_metric_values"][0] = 0.0
        does_chiller_performance_match_curve(TEST_CHILLER_ZERO_EFFI, "AA")


def test__does_chiller_performance_match_curve__zero_capacity():
    with pytest.raises(
        RCTFailureException,
        match="The 'capacity' value must be greater than 0 W.",
    ):
        TEST_CHILLER_ZERO_EFFI = copy.deepcopy(TEST_CHILLER)
        TEST_CHILLER_ZERO_EFFI["capacity_operating_points"][0]["capacity"] = 0.0
        does_chiller_performance_match_curve(TEST_CHILLER_ZERO_EFFI, "AA")
