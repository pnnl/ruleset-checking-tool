from typing import TypedDict

from pint import Quantity
from rct229.rulesets.ashrae9012019.data_fns.table_lighting_space_type_BPF_area_type_map import (
    lighting_space_type_to_BPF_area_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_BPF_BAT import (
    get_zone_BPF_BAT,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO


class ClassificationType:
    BUILDING_SEGMENT_LIGHTING: str = "BUILDING_SEGMENT_LIGHTING"
    SPACE_LIGHTING: str = "SPACE_LIGHTING"


class BuildingAreaTypeWithTotalAreaAndZone(TypedDict):
    zone_id: list[str]
    area: Quantity
    classification_source: str


def get_BPF_building_area_types_and_zones(
    rmd: dict,
) -> dict[str, BuildingAreaTypeWithTotalAreaAndZone]:
    """
    Get a dictionary of the zone_ids associated with each BPF building area type associated with U_RMD, P_RMD, or B_RMD. Also returns the total floor area of each building area type and the source of the information (BUILDING_AREA_LIGHTING or SPACE_LIGHTING)

    Parameters
    ----------
    rmd: str, The ruleset model descriptions

    Returns
    -------
    building_area_types_with_total_area_and_zones_dict: A dict that saves all the BPF building area types and includes a list of all the zone ids associated with area type as well as
                                                        the total area of each building area type: {MULTIFAMILY: {"zone_id": ["zone_2", "zone_3", "zone_4"], "area": 34567, "classification_source": "BUILDING_SEGMENT_LIGHTING"}, HEALTHCARE_HOSPITAL: {"zone_id": ["zone_1","zone_5","zone_6"], "area": 20381, "classification_source": "SPACE_LIGHTING"}
    """

    building_area_types_with_total_area_and_zones_dict = {}
    for building_segment in find_all("$.buildings[*].building_segments[*]", rmd):
        if building_segment.get(
            "lighting_building_area_type"
        ) is not None and building_segment[
            "lighting_building_area_type"
        ] != lighting_space_type_to_BPF_area_type(
            "NONE"
        ):
            building_segment_BPF_BAT = lighting_space_type_to_BPF_area_type(
                building_segment["lighting_building_area_type"]
            )
        else:
            building_segment_BPF_BAT = None

        # when `lighting_building_area_type` key does NOT exist
        if building_segment_BPF_BAT is None:
            for zone in find_all("$.zones[*]", building_segment):
                zone_BPF_BAT_dict = get_zone_BPF_BAT(rmd, zone["id"])

                # find the key that has the greatest value
                building_segment_BPF_BAT = max(
                    zone_BPF_BAT_dict,
                    key=lambda k: zone_BPF_BAT_dict[k],
                )

                if (
                    building_segment_BPF_BAT
                    not in building_area_types_with_total_area_and_zones_dict
                ):
                    building_area_types_with_total_area_and_zones_dict[
                        building_segment_BPF_BAT
                    ] = {
                        "zone_id": [],
                        "area": ZERO.AREA,
                        "classification_source": ClassificationType.SPACE_LIGHTING,
                    }

                building_area_types_with_total_area_and_zones_dict[
                    building_segment_BPF_BAT
                ]["zone_id"].append(zone["id"])
                building_area_types_with_total_area_and_zones_dict[
                    building_segment_BPF_BAT
                ]["area"] += sum(area for area in zone_BPF_BAT_dict.values())
                building_area_types_with_total_area_and_zones_dict[
                    building_segment_BPF_BAT
                ]["classification_source"] = ClassificationType.SPACE_LIGHTING

        # when `lighting_building_area_type` key exists
        else:
            if (
                building_segment_BPF_BAT
                not in building_area_types_with_total_area_and_zones_dict
            ):
                building_area_types_with_total_area_and_zones_dict[
                    building_segment_BPF_BAT
                ] = {
                    "zone_id": [],
                    "area": ZERO.AREA,
                    "classification_source": ClassificationType.BUILDING_SEGMENT_LIGHTING,
                }

            for zone in find_all("$.zones[*]", building_segment):
                building_area_types_with_total_area_and_zones_dict[
                    building_segment_BPF_BAT
                ]["zone_id"].append(zone["id"])
                building_area_types_with_total_area_and_zones_dict[
                    building_segment_BPF_BAT
                ]["area"] += sum(
                    space.get("floor_area", ZERO.AREA)
                    for space in find_all("$.spaces[*]", zone)
                )

    assert_(
        building_area_types_with_total_area_and_zones_dict,
        "Cannot find/identify building area type in the "
        "project, Require at least one but got None. Check "
        "your inputs.",
    )
    return building_area_types_with_total_area_and_zones_dict
