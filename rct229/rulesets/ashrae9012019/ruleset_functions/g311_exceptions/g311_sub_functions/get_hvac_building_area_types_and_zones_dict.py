import logging
from typing import TypedDict

from pint import Quantity
from pydash import curry, filter_, flatten_deep, flow, map_
from rct229.rulesets.ashrae9012019.data_fns.table_lighting_to_hvac_bat_map_fns import (
    building_lighting_to_hvac_bat,
    space_lighting_to_hvac_bat,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
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

# create currier that merges two building area type values
bat_val_merge_curry = curry(
    lambda a, b: {
        "zone_ids": [*a["zone_ids"], *b["zone_ids"]],
        "floor_area": a["floor_area"] + b["floor_area"],
    }
)
# create currier that retrieves a data form a dictionary with
# default handling of non-existence errors.
get_bat_val_func_curry = curry(
    lambda bat_dict, key: bat_dict.get(key, {"zone_ids": [], "floor_area": ZERO.AREA})
)


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

    building_area_types_with_total_area_and_zones_dict = {}
    # create a new currier to get building area type value from building_area_types_with_total_area_and_zones_dict
    bat_dict_currier = get_bat_val_func_curry(
        building_area_types_with_total_area_and_zones_dict
    )

    for building_segment in find_all("$.buildings[*].building_segments[*]", rmd):
        if building_segment.get(
            "area_type_heating_ventilating_air_conditioning_system"
        ):
            building_segment_hvac_bat = building_segment[
                "area_type_heating_ventilating_air_conditioning_system"
            ]
            classification_source = ClassificationSource.BUILDING_SEGMENT_HVAC_BAT
        elif building_segment.get("lighting_building_area_type"):
            building_segment_hvac_bat = building_lighting_to_hvac_bat(
                building_segment["lighting_building_area_type"]
            )
            classification_source = ClassificationSource.BUILDING_SEGMENT_LIGHTING
        else:
            building_segment_space_types_areas_dict = {}
            for space in find_all("$.zones[*].spaces[*]", building_segment):
                space_hvac_bat = space.get("lighting_space_type")
                if space_hvac_bat:
                    building_segment_space_types_areas_dict[
                        space_hvac_bat
                    ] = building_segment_space_types_areas_dict.get(
                        space_hvac_bat, ZERO.AREA
                    ) + space.get(
                        "floor_area", ZERO.AREA
                    )

            # Raise assertion if no space type matched from data (empty dictionary)
            assert_(
                building_segment_space_types_areas_dict,
                f"Failed to determine hvac area type for building segment: {building_segment['id']}. Verify the model inputs and make sure it contains either of area_type_heating_ventilating_air_conditioning_system, lighting_building_area_type or space.lighting_space_type.",
            )

            building_segment_hvac_bat = space_lighting_to_hvac_bat(
                max(
                    building_segment_space_types_areas_dict,
                    key=building_segment_space_types_areas_dict.get,
                )
            )
            classification_source = ClassificationSource.SPACE_LIGHTING

        # Log the data for debug purpose
        logger.info(
            f"building segment {building_segment['id']} is determined as {building_segment_hvac_bat}. The classification source is {classification_source}"
        )

        # filter zones
        # only conditioned (mixed, residential & nonresidential) zones in this list.
        filtered_zones_list = filter_(
            find_all("$.zones[*]", building_segment),
            lambda zone: zone_conditioning_category_dict[zone["id"]]
            in [
                ZoneConditioningCategory.CONDITIONED_MIXED,
                ZoneConditioningCategory.CONDITIONED_NON_RESIDENTIAL,
                ZoneConditioningCategory.CONDITIONED_RESIDENTIAL,
            ],
        )

        if filtered_zones_list:
            # if there are conditioned zones
            # add new hvac bat val to the existing/new hvac bat
            building_area_types_with_total_area_and_zones_dict[
                building_segment_hvac_bat
            ] = flow(
                bat_dict_currier,
                bat_val_merge_curry(
                    {
                        "zone_ids": map_(filtered_zones_list, "id"),
                        "floor_area": flow(
                            # create a 2d list [[zone -> space floor area list]]
                            lambda zones: map_(
                                zones,
                                lambda zone: find_all("$.spaces[*].floor_area", zone),
                            ),
                            flatten_deep,
                            sum,
                        )(filtered_zones_list),
                    }
                ),
            )(
                building_segment_hvac_bat
            )

    # check other undetermined
    if OTHER_UNDETERMINED in building_area_types_with_total_area_and_zones_dict:
        # find predominate hvac bat by the largest floor_area
        predominate_hvac_bat = sorted(
            building_area_types_with_total_area_and_zones_dict.items(),
            key=lambda x: x[1]["floor_area"],
            reverse=True,
        )[0][0]
        # pop the OTHER UNDETERMINED val
        other_undetermined_val = building_area_types_with_total_area_and_zones_dict.pop(
            OTHER_UNDETERMINED
        )
        # create currier for building area types value merge with other undetermined data
        other_undetermined_bat_val_merge_currier = bat_val_merge_curry(
            other_undetermined_val
        )
        # create a new flow to add/update building area types value with the other undetermined data.
        assign_bat_val_flow = flow(
            bat_dict_currier, other_undetermined_bat_val_merge_currier
        )

        if (
            predominate_hvac_bat == OTHER_UNDETERMINED
            or predominate_hvac_bat == HVAC_BUILDING_AREA_TYPE_OPTIONS.RESIDENTIAL
        ):
            # case to merge other undetermined to other non residential
            building_area_types_with_total_area_and_zones_dict[
                HVAC_BUILDING_AREA_TYPE_OPTIONS.OTHER_NON_RESIDENTIAL
            ] = assign_bat_val_flow(
                HVAC_BUILDING_AREA_TYPE_OPTIONS.OTHER_NON_RESIDENTIAL
            )
        else:
            # case to merge other undetermined to predominate hvac bat
            building_area_types_with_total_area_and_zones_dict[
                predominate_hvac_bat
            ] = assign_bat_val_flow(predominate_hvac_bat)

    assert_(
        building_area_types_with_total_area_and_zones_dict,
        "No building area is found in the model. Please make "
        "sure there are building_segments data group in the "
        "model",
    )
    return building_area_types_with_total_area_and_zones_dict
