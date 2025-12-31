import logging
from typing import TypedDict

from pint import Quantity
from rct229.rulesets.ashrae9012022.data_fns.table_lighting_to_hvac_bat_map_fns import (
    building_lighting_to_hvac_bat,
    space_lighting_to_hvac_bat,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory,
    get_zone_conditioning_category_rmd_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

OTHER_UNDETERMINED = "OTHER_UNDETERMINED"
HVAC_BUILDING_AREA_TYPE_OPTIONS = SchemaEnums.schema_enums[
    "HeatingVentilatingAirConditioningBuildingAreaOptions2019ASHRAE901"
]


class ClassificationSource:
    BUILDING_SEGMENT_HVAC_BAT = "BUILDING_SEGMENT_HVAC_BAT"
    BUILDING_SEGMENT_LIGHTING = "BUILDING_SEGMENT_LIGHTING"
    SPACE_LIGHTING = "SPACE_LIGHTING"


logger = logging.getLogger(__name__)


class BuildingAreaTypesWithTotalAreaZones(TypedDict):
    floor_area: Quantity
    zone_ids: list[str]


def get_hvac_building_area_types_and_zones_dict(
    climate_zone: str, rmd: dict
) -> dict[str, BuildingAreaTypesWithTotalAreaZones]:
    """

    Parameters
    ----------
    climate_zone str
        One of the ClimateZoneOptions2019ASHRAE901 enumerated values
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema

    Returns
    -------

    """
    zone_conditioning_category_dict = get_zone_conditioning_category_rmd_dict(
        climate_zone, rmd
    )

    result: dict[str, BuildingAreaTypesWithTotalAreaZones] = {}

    def get_bat_val(key):
        return result.get(key, {"zone_ids": [], "floor_area": ZERO.AREA})

    def merge(a, b):
        return {
            "zone_ids": a["zone_ids"] + b["zone_ids"],
            "floor_area": a["floor_area"] + b["floor_area"],
        }

    for building_segment in find_all("$.buildings[*].building_segments[*]", rmd):

        # ----------------------------------------------------------
        # Determine HVAC BAT
        # ----------------------------------------------------------
        if building_segment.get(
            "area_type_heating_ventilating_air_conditioning_system"
        ):
            hvac_bat = building_segment[
                "area_type_heating_ventilating_air_conditioning_system"
            ]
            source = ClassificationSource.BUILDING_SEGMENT_HVAC_BAT

        elif building_segment.get("lighting_building_area_type"):
            hvac_bat = building_lighting_to_hvac_bat(
                building_segment["lighting_building_area_type"]
            )
            source = ClassificationSource.BUILDING_SEGMENT_LIGHTING

        else:
            space_area_by_type = {}

            for space in find_all("$.zones[*].spaces[*]", building_segment):
                space_type = space.get("lighting_space_type")
                if space_type:
                    space_area_by_type[space_type] = space_area_by_type.get(
                        space_type, ZERO.AREA
                    ) + space.get("floor_area", ZERO.AREA)

            assert_(
                space_area_by_type,
                f"Failed to determine hvac area type for building segment "
                f"{building_segment['id']}. Verify the model inputs.",
            )

            dominant_space_type = max(space_area_by_type, key=space_area_by_type.get)
            hvac_bat = space_lighting_to_hvac_bat(dominant_space_type)
            source = ClassificationSource.SPACE_LIGHTING

        logger.info(
            f"building segment {building_segment['id']} is determined as "
            f"{hvac_bat}. The classification source is {source}"
        )

        # ----------------------------------------------------------
        # Collect conditioned zones
        # ----------------------------------------------------------
        zone_ids = []
        total_area = ZERO.AREA

        for zone in building_segment.get("zones", []):
            if zone_conditioning_category_dict.get(zone["id"]) in {
                ZoneConditioningCategory.CONDITIONED_MIXED,
                ZoneConditioningCategory.CONDITIONED_NON_RESIDENTIAL,
                ZoneConditioningCategory.CONDITIONED_RESIDENTIAL,
            }:
                zone_ids.append(zone["id"])
                for space in zone.get("spaces", []):
                    total_area += space.get("floor_area", ZERO.AREA)

        if not zone_ids:
            continue

        result[hvac_bat] = merge(
            get_bat_val(hvac_bat),
            {"zone_ids": zone_ids, "floor_area": total_area},
        )

    # ------------------------------------------------------------------
    # Handle OTHER_UNDETERMINED
    # ------------------------------------------------------------------
    if OTHER_UNDETERMINED in result:
        predominate_bat = max(result.items(), key=lambda x: x[1]["floor_area"])[0]

        other_val = result.pop(OTHER_UNDETERMINED)

        if (
            predominate_bat == OTHER_UNDETERMINED
            or predominate_bat == HVAC_BUILDING_AREA_TYPE_OPTIONS.RESIDENTIAL
        ):
            target = HVAC_BUILDING_AREA_TYPE_OPTIONS.OTHER_NON_RESIDENTIAL
        else:
            target = predominate_bat

        result[target] = merge(get_bat_val(target), other_val)

    assert_(
        result,
        "No building area is found in the model. "
        "Please make sure there are building_segments data group in the model",
    )

    return result
