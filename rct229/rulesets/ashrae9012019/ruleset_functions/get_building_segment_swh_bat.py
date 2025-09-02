from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import (
    find_exactly_one_building_segment,
    find_exactly_one_service_water_heating_use,
    find_exactly_one_space,
)

SERVICE_WATER_HEATING_USE_UNIT = SchemaEnums.schema_enums[
    "ServiceWaterHeatingUseUnitOptions"
]


def get_building_segment_swh_bat(rmd: dict, building_segment_id: str) -> str:
    """
    This function determines the SWH BAT for the given building segment.
    Returns None if there is no service water heating uses and no service_water_heating_area_type under building segment,
    UNDETERMINED if there are service water heating uses but no service_water_heating_area_type under building segment,
    A bat type if there is service_water_heating_area_type under building segment

    Parameters
    ----------
    rmd: dict
        RMD at RuleSetModelDescription level
    building_segment_id: str
        building segment id

    Returns
    -------
    building_segment_swh_bat: str
        one of the ServiceWaterHeatingSpaceOptions2019ASHRAE901 options. If `service_water_heating_uses` key has no `use_units` or the `use_units` is SERVICE_WATER_HEATING_USE_UNIT.OTHER, the function returns UNDETERMINED string.

    """

    building_segment = find_exactly_one_building_segment(rmd, building_segment_id)
    building_segment_swh_bat = building_segment.get(
        "service_water_heating_area_type", "UNDETERMINED"
    )

    if building_segment_swh_bat == "UNDETERMINED":
        swh_use_dict = {}
        bldg_seg_id = building_segment["id"]
        swh_uses_from_spaces = find_all(
            f'$.buildings[*].building_segments[*][?(@.id = "{bldg_seg_id}")].zones[*].spaces[*].service_water_heating_uses[*]',
            rmd,
        )
        swh_uses_from_building_segment = find_all(
            f'$.buildings[*].building_segments[*][?(@.id = "{bldg_seg_id}")].service_water_heating_uses[*]',
            rmd,
        )
        swh_uses_all = list(set(swh_uses_from_spaces + swh_uses_from_building_segment))

        for swh_use_id in swh_uses_all:
            swh_use = find_exactly_one_service_water_heating_use(rmd, swh_use_id)
            if (
                swh_use
                and swh_use.get("use_units") == SERVICE_WATER_HEATING_USE_UNIT.OTHER
            ):
                building_segment_swh_bat = "UNDETERMINED"

            swh_use_energy_by_space = get_energy_required_to_heat_swh_use(
                swh_use_id, rmd, building_segment["id"]
            )

            if swh_use.get("area_type"):
                swh_use_dict.setdefault(swh_use["area_type"], 0)
                swh_use_dict[swh_use["area_type"]] += sum(
                    v for v in swh_use_energy_by_space.values() if v is not None
                )
            else:
                for space_id in swh_use_energy_by_space:
                    space = find_exactly_one_space(rmd, space_id)
                    if space.get("service_water_heating_area_type"):
                        swh_use_dict.setdefault(
                            space["service_water_heating_area_type"], 0
                        )
                        swh_use_dict[space["service_water_heating_area_type"]] += (
                            swh_use_energy_by_space[space_id]
                            if swh_use_energy_by_space[space_id] is not None
                            else 0
                        )
                    else:
                        swh_use_dict.setdefault("UNDETERMINED", 0)
                        swh_use_dict["UNDETERMINED"] += (
                            swh_use_energy_by_space[space_id]
                            if swh_use_energy_by_space[space_id] is not None
                            else 0
                        )

        total_energy = sum(swh_use_dict.values())
        assigned_energy = total_energy - swh_use_dict.get("UNDETERMINED", 0)
        known_area_types = [k for k in swh_use_dict if k != "UNDETERMINED"]

        # If less than 50% of energy is assigned to a known area type
        if assigned_energy < 0.5 * total_energy:
            building_segment_swh_bat = "UNDETERMINED"
        # If more than one know SWH area type exists
        elif len(known_area_types) > 1:
            building_segment_swh_bat = "UNDETERMINED"
        else:
            assert_(
                len(known_area_types) > 0,
                "At least one building area type must exist other than UNDETERMINED",
            )

            building_segment_swh_bat = known_area_types[0]

    return building_segment_swh_bat
