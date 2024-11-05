from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.pint_utils import ZERO

SERVICE_WATER_HEATING_USE_UNIT = SchemaEnums.schema_enums[
    "ServiceWaterHeatingUseUnitOptions"
]


def get_building_segment_swh_bat(
    rmd: dict, building_segment_id: str, is_leap_year: bool = False
) -> str:
    """
    This function determines the SWH BAT for the given building segment.

    Parameters
    ----------
    rmd: dict
        RMD at RuleSetModelDescription level
    building_segment_id: str
        building segment id
    is_leap_year: bool, default: False
        Whether the year is a leap year or not.

    Returns
    -------
    building_segment_swh_bat: str
        one of the ServiceWaterHeatingSpaceOptions2019ASHRAE901 options

    """

    building_segment = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*]",
        "id",
        building_segment_id,
        rmd,
    )

    if building_segment.get("service_water_heating_building_area_type"):
        building_segment_swh_bat = building_segment[
            "service_water_heating_building_area_type"
        ]
    else:
        swh_use_dict = {}
        for swh_use_id in find_all(
            f'$.buildings[*].building_segments[*][?(@.id="{building_segment["id"]}")].zones[*].spaces[*].service_water_heating_uses[*].id',
            rmd,
        ):
            swh_use = find_exactly_one_with_field_value(
                f"$.zones[*].spaces[*].service_water_heating_uses[*]",
                "id",
                swh_use_id,
                building_segment,
            )

            if (
                not swh_use
                or swh_use.get("use_units") == SERVICE_WATER_HEATING_USE_UNIT.OTHER
            ):
                return None

            swh_use_energy_by_space = get_energy_required_to_heat_swh_use(
                swh_use["id"], rmd, building_segment["id"], is_leap_year
            )

            if swh_use.get("area_type"):
                area_type = swh_use["area_type"]
                swh_use_dict.setdefault(area_type, ZERO.ENERGY)
                swh_use_dict[area_type] += sum(swh_use_energy_by_space.values())
            else:
                for space_id in swh_use_energy_by_space:
                    if space_id != "no_spaces_assigned":
                        space = find_exactly_one_with_field_value(
                            "$.zones[*].spaces[*]",
                            "id",
                            space_id,
                            building_segment,
                        )
                        if space.get("service_water_heating_building_area_type"):
                            service_water_heating_bat = space[
                                "service_water_heating_building_area_type"
                            ]
                            swh_use_dict.setdefault(
                                service_water_heating_bat, ZERO.ENERGY
                            )
                            swh_use_dict[
                                service_water_heating_bat
                            ] += swh_use_energy_by_space[space_id]
                        else:
                            swh_use_dict.setdefault("UNDETERMINED", ZERO.ENERGY)
                            swh_use_dict["UNDETERMINED"] += swh_use_energy_by_space[
                                space_id
                            ]

        building_segment_swh_bat = (
            max(swh_use_dict, key=swh_use_dict.get) if swh_use_dict else None
        )

    return building_segment_swh_bat
