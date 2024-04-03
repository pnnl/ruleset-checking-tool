from typing import TypedDict

from pint import Quantity
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_BPF_BAT import (
    get_zone_BPF_BAT,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

LIGHTING_BUILDING_AREA = SchemaEnums.schema_enums[
    "LightingBuildingAreaOptions2019ASHRAE901T951TG38"
]


LIGHTING_BUILDING_AREA_LOOKUP = {
    LIGHTING_BUILDING_AREA.AUTOMOTIVE_FACILITY: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.CONVENTION_CENTER: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.COURTHOUSE: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.DINING_BAR_LOUNGE_LEISURE: "RESTAURANT",
    LIGHTING_BUILDING_AREA.DINING_CAFETERIA_FAST_FOOD: "RESTAURANT",
    LIGHTING_BUILDING_AREA.DINING_FAMILY: "RESTAURANT",
    LIGHTING_BUILDING_AREA.DORMITORY: "MULTIFAMILY",
    LIGHTING_BUILDING_AREA.EXERCISE_CENTER: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.FIRE_STATION: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.GYMNASIUM: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.HEALTH_CARE_CLINIC: "HEALTHCARE_HOSPITAL",
    LIGHTING_BUILDING_AREA.HOSPITAL: "HEALTHCARE_HOSPITAL",
    LIGHTING_BUILDING_AREA.HOTEL_MOTEL: "HOTEL_MOTEL",
    LIGHTING_BUILDING_AREA.LIBRARY: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.MANUFACTURING_FACILITY: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.MULTIFAMILY: "MULTIFAMILY",
    LIGHTING_BUILDING_AREA.MUSEUM: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.OFFICE: "OFFICE",
    LIGHTING_BUILDING_AREA.PARKING_GARAGE: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.PENITENTIARY: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.PERFORMING_ARTS_THEATER: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.POLICE_STATION: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.POST_OFFICE: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.RELIGIOUS_FACILITY: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.RETAIL: "RETAIL",
    LIGHTING_BUILDING_AREA.SCHOOL_UNIVERSITY: "SCHOOL",
    LIGHTING_BUILDING_AREA.SPORTS_ARENA: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.TOWN_HALL: "OFFICE",
    LIGHTING_BUILDING_AREA.TRANSPORTATION: "ALL_OTHER",
    LIGHTING_BUILDING_AREA.WAREHOUSE: "WAREHOUSE",
    LIGHTING_BUILDING_AREA.WORKSHOP: "WAREHOUSE",
    LIGHTING_BUILDING_AREA.NONE: "NONE",
}


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
        if (
            building_segment.get("lighting_building_area_type") is not None
            and building_segment["lighting_building_area_type"]
            != LIGHTING_BUILDING_AREA.NONE
        ):
            building_segment_BPF_BAT = LIGHTING_BUILDING_AREA_LOOKUP[
                building_segment["lighting_building_area_type"]
            ]
            classification_source = "BUILDING_SEGMENT_LIGHTING"
        else:
            building_segment_space_types_areas_dict = {}
            building_segment_BPF_BAT = {}
            for zone in find_all("$.zones[*]", building_segment):
                zone_id = zone["id"]
                zone_BPF_BAT_dict = get_zone_BPF_BAT(rmd, zone_id)

                # merge zone_BPF_BAT_dict and building_segment_space_types_areas_dict
                # if the two dicts have the same keys, add the two values
                building_segment_space_types_areas_dict.update(
                    {
                        key: building_segment_space_types_areas_dict.get(key, ZERO.AREA)
                        + zone_BPF_BAT_dict.get(key, ZERO.AREA)
                        for key in set(building_segment_space_types_areas_dict)
                        | set(zone_BPF_BAT_dict)
                    }
                )

                # find the key that has the greatest value
                building_segment_BPF_BAT[zone_id] = max(
                    building_segment_space_types_areas_dict,
                    key=lambda k: building_segment_space_types_areas_dict[k],
                )
            classification_source = "SPACE_LIGHTING"

        for zone in find_all("$.zones[*]", building_segment):
            zone_id = zone["id"]
            building_segment_BPF_BAT_zone = (
                building_segment_BPF_BAT[zone_id]
                if classification_source == "SPACE_LIGHTING"
                else building_segment_BPF_BAT
            )
            if (
                building_segment_BPF_BAT_zone
                not in building_area_types_with_total_area_and_zones_dict
            ):
                building_area_types_with_total_area_and_zones_dict[
                    building_segment_BPF_BAT_zone
                ] = {
                    "zone_id": [],
                    "area": ZERO.AREA,
                    "classification_source": classification_source,
                }

            building_area_types_with_total_area_and_zones_dict[
                building_segment_BPF_BAT_zone
            ]["zone_id"].append(zone_id)

            building_area_types_with_total_area_and_zones_dict[
                building_segment_BPF_BAT_zone
            ]["area"] += sum(
                [
                    space.get("floor_area", ZERO.AREA)
                    for space in find_all("$.spaces[*]", zone)
                ]
            )

    return building_area_types_with_total_area_and_zones_dict
