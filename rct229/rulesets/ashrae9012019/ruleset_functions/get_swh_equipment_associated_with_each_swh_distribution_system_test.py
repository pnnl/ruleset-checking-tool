from dataclasses import dataclass, field
from typing import List

from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_associated_with_each_swh_distriubtion_system import (
    get_swh_equipment_associated_with_each_swh_distribution_system,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

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
                                    "service_water_heating_uses": ["SWH Use 1"],
                                },
                                {
                                    "id": "Space 2",
                                    "service_water_heating_uses": ["SWH Use 2"],
                                },
                                {
                                    "id": "Space 3",
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    ],
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "served_by_distribution_system": "SWH Distribution 1",
        },
        {
            "id": "SWH Use 2",
            "served_by_distribution_system": "SWH Distribution 1",
        },
    ],
    "service_water_heating_distribution_systems": [
        {
            "id": "SWH Distribution 1",
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
    "pumps": [
        {
            "id": "Pump 1",
            "loop_or_piping": "SWH Piping 1",
        },
        {
            "id": "Pump 3",
            "loop_or_piping": "HVAC Piping 1",
        },
    ],
    "service_water_heating_equipment": [
        {
            "id": "SWH Equipment 1",
            "distribution_system": "SWH Distribution 1",
            "solar_thermal_systems": [
                {
                    "id": "Solar Thermal System 1",
                },
                {
                    "id": "Solar Thermal System 2",
                },
            ],
        },
        {
            "id": "SWH Equipment 2",
            "distribution_system": "SWH Distribution 2",
            "solar_thermal_systems": [
                {
                    "id": "Solar Thermal System 3",
                },
                {
                    "id": "Solar Thermal System 4",
                },
            ],
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


@dataclass
class SWHDistributionAssociations:
    swh_heating_eq: List[str] = field(default_factory=list)
    pumps: List[str] = field(default_factory=list)
    tanks: List[str] = field(default_factory=list)
    piping: List[str] = field(default_factory=list)
    solar_thermal: List[str] = field(default_factory=list)
    uses: List[str] = field(default_factory=list)
    spaces_served: List[str] = field(default_factory=list)


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_get_swh_equipment_associated_with_each_swh_distribution_system():
    swh_and_equip_dict = get_swh_equipment_associated_with_each_swh_distribution_system(
        TEST_RMD
    )
    assert len(swh_and_equip_dict) == 1
    assert swh_and_equip_dict["SWH Distribution 1"].swh_heating_eq == [
        "SWH Equipment 1"
    ]
    assert swh_and_equip_dict["SWH Distribution 1"].pumps == ["Pump 1"]
    assert swh_and_equip_dict["SWH Distribution 1"].tanks == ["Tank 1", "Tank 2"]
    assert swh_and_equip_dict["SWH Distribution 1"].piping == [
        "SWH Piping 1",
        "SWH Piping Child 1",
        "SWH Piping 1-a",
        "SWH Piping 1-b",
    ]
    assert swh_and_equip_dict["SWH Distribution 1"].solar_thermal == [
        "Solar Thermal System 1",
        "Solar Thermal System 2",
    ]
    assert swh_and_equip_dict["SWH Distribution 1"].uses == ["SWH Use 1", "SWH Use 2"]
    assert swh_and_equip_dict["SWH Distribution 1"].spaces_served == [
        "Space 1",
        "Space 2",
    ]
