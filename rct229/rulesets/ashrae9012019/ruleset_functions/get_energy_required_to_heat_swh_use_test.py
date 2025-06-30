from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd
from rct229.utils.jsonpath_utils import (
    find_exactly_one_with_field_value,
)
from rct229.utils.std_comparisons import std_equal

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "service_water_heating_uses": [
                                        "SWH Use 1",
                                        "SWH Use 2",
                                        "SWH Use 3",
                                        "SWH Use 4",
                                    ],
                                    "number_of_occupants": 5,
                                    "floor_area": 100,
                                },
                                {
                                    "id": "Space 2",
                                    "service_water_heating_uses": [
                                        "SWH Use 5",
                                        "SWH Use 6",
                                        "SWH Use 7",
                                    ],
                                    "number_of_occupants": 5,
                                    "floor_area": 100,
                                },
                                {
                                    "id": "Space 3",
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": "Building Segment 2",
                    "zones": [
                        {
                            "id": "Thermal Zone 2",
                        }
                    ],
                },
            ],
        }
    ],
    "schedules": [
        {
            "id": "SWH Schedule 1",
            "hourly_values": [0.8] * 8760,
        },
        {
            "id": "SWH Entering Water Temp Schedule 1",
            "hourly_values": [50] * 8760,
        },
    ],
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "use": 100,
            "use_units": "POWER_PER_PERSON",
            "is_heat_recovered_by_drain": True,
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "SWH Use 2",
            "use": 10,
            "use_units": "POWER_PER_AREA",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "SWH Use 3",
            "use": 1000,
            "use_units": "POWER",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "SWH Use 4",
            "use": 100,
            "use_units": "VOLUME_PER_PERSON",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "SWH Use 5",
            "use": 10,
            "use_units": "VOLUME_PER_AREA",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "SWH Use 6",
            "use": 1000,
            "use_units": "VOLUME",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "SWH Use 7",
            "use": 10,
            "use_units": "OTHER",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
    ],
    "service_water_heating_distribution_systems": [
        {
            "id": "SWH Distribution 1",
            "design_supply_temperature": 60,
            "drain_heat_recovery_efficiency": 0.3,
            "entering_water_mains_temperature_schedule": "SWH Entering Water Temp Schedule 1",
            "tanks": [
                {
                    "id": "Tank 1",
                },
                {
                    "id": "Tank 2",
                },
            ],
            "service_water_piping": {
                "id": "SWH Piping 1",
                "child": [
                    {
                        "id": "SWH Piping Child 1",
                        "child": [
                            {
                                "id": "SWH Piping 1-a",
                            },
                            {
                                "id": "SWH Piping 1-b",
                            },
                        ],
                    }
                ],
            },
        }
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
}

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]

TEST_BUILDING_SEGMENT = find_exactly_one_with_field_value(
    "$.buildings[*].building_segments[*]",
    "id",
    "Building Segment 1",
    TEST_RMD,
)

TEST_BUILDING_SEGMENT_NO_SWH_USE = find_exactly_one_with_field_value(
    "$.buildings[*].building_segments[*]",
    "id",
    "Building Segment 2",
    TEST_RMD,
)


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_energy_required_to_heat_swh_use_power_per_person():
    energy_required_by_space = get_energy_required_to_heat_swh_use(
        "SWH Use 1", TEST_RMD, "Building Segment 1"
    )
    assert len(energy_required_by_space) == 1 and std_equal(
        energy_required_by_space["Space 1"], 8362628.17 * ureg("Btu")
    )


def test__get_energy_required_to_heat_swh_use_power_per_area():
    energy_required_by_space = get_energy_required_to_heat_swh_use(
        "SWH Use 2", TEST_RMD, "Building Segment 1"
    )
    assert len(energy_required_by_space) == 1 and std_equal(
        energy_required_by_space["Space 1"], 23912285.2 * ureg("Btu")
    )


def test__get_energy_required_to_heat_swh_use_power():
    energy_required_by_space = get_energy_required_to_heat_swh_use(
        "SWH Use 3", TEST_RMD, "Building Segment 1"
    )
    assert len(energy_required_by_space) == 1 and std_equal(
        energy_required_by_space["Space 1"], 23912285.2 * ureg("Btu")
    )


def test__get_energy_required_to_heat_swh_use_volume_per_person():
    energy_required_by_space = get_energy_required_to_heat_swh_use(
        "SWH Use 4", TEST_RMD, "Building Segment 1"
    )
    assert len(energy_required_by_space) == 1 and std_equal(
        energy_required_by_space["Space 1"], 139200741 * ureg("Btu")
    )


def test__get_energy_required_to_heat_swh_use_volume_per_area():
    energy_required_by_space = get_energy_required_to_heat_swh_use(
        "SWH Use 5", TEST_RMD, "Building Segment 1"
    )
    assert len(energy_required_by_space) == 1 and std_equal(
        energy_required_by_space["Space 2"], 278401481.1 * ureg("Btu")
    )


def test__get_energy_required_to_heat_swh_use_volume():
    energy_required_by_space = get_energy_required_to_heat_swh_use(
        "SWH Use 6", TEST_RMD, "Building Segment 1"
    )
    assert len(energy_required_by_space) == 1 and std_equal(
        energy_required_by_space["Space 2"], 278401481 * ureg("Btu")
    )


def test__get_energy_required_to_heat_swh_use_other():
    energy_required_by_space = get_energy_required_to_heat_swh_use(
        "SWH Use 7", TEST_RMD, "Building Segment 1"
    )
    assert (
        len(energy_required_by_space) == 1
        and energy_required_by_space["Space 2"] is None
    )
