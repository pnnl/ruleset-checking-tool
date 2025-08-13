from typing import TypedDict

from pint import Quantity
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    ZoneConditioningDataDict,
    get_surface_conditioning_category_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR


def get_building_scc_skylight_roof_ratios_dict(
    climate_zone: str, constructions: list, building: dict
) -> ZoneConditioningDataDict:
    """Gets a dictionary mapping skylight and envelope roof ratios for a building for residential, non-residential,
    mixed and semi-heated surface conditioning categories
            Parameters
            ----------
            climate_zone : str
                One of the ClimateZoneOptions2019ASHRAE901 enumerated values
            constructions : list
                A list of construction dictionaries as defined by the ASHRAE229 schema
            building : dict
                A dictionary representing a building as defined by the ASHRAE229 schema
            Returns
            -------
            dict
                A dictionary that saves each surface conditioning category (residential, non-residential, mixed and semi-heated)
                with its skylight-roof-ratios for each building in rmd.
                {
                    "building_id": {"EXTERIOR RESIDENTIAL": srr_res, "EXTERIOR NON-RESIDENTIAL": srr_nonres,
                    "EXTERIOR MIXED": srr_mixed, "SEMI-EXTERIOR": srr_semiheated},
                }
    """
    # required fields for this function are coming from the nested functions
    scc_dictionary = get_surface_conditioning_category_dict(
        climate_zone, building, constructions
    )
    total_res_roof_area = ZERO.AREA
    total_res_skylight_area = ZERO.AREA
    total_nonres_roof_area = ZERO.AREA
    total_nonres_skylight_area = ZERO.AREA
    total_mixed_roof_area = ZERO.AREA
    total_mixed_skylight_area = ZERO.AREA
    total_semiheated_roof_area = ZERO.AREA
    total_semiheated_skylight_area = ZERO.AREA

    for surface in find_all("building_segments[*].zones[*].surfaces[*]", building):
        if get_opaque_surface_type(surface) == OST.ROOF:
            roof_area = getattr_(surface, "surface", "area")
            skylight_area = _helper_calculate_skylight_area(surface)
            if scc_dictionary[surface["id"]] == SCC.EXTERIOR_RESIDENTIAL:
                total_res_roof_area += roof_area
                total_res_skylight_area += skylight_area
            elif scc_dictionary[surface["id"]] == SCC.EXTERIOR_NON_RESIDENTIAL:
                total_nonres_roof_area += roof_area
                total_nonres_skylight_area += skylight_area
            elif scc_dictionary[surface["id"]] == SCC.EXTERIOR_MIXED:
                total_mixed_roof_area += roof_area
                total_mixed_skylight_area += skylight_area
            elif scc_dictionary[surface["id"]] == SCC.SEMI_EXTERIOR:
                total_semiheated_roof_area += roof_area
                total_semiheated_skylight_area += skylight_area

    srr_res = 0.0
    srr_nonres = 0.0
    srr_mixed = 0.0
    srr_semiheated = 0.0
    if total_res_roof_area > ZERO.AREA:
        srr_res = total_res_skylight_area / total_res_roof_area
    if total_nonres_roof_area > ZERO.AREA:
        srr_nonres = total_nonres_skylight_area / total_nonres_roof_area
    if total_mixed_roof_area > ZERO.AREA:
        srr_mixed = total_mixed_skylight_area / total_mixed_roof_area
    if total_semiheated_roof_area > ZERO.AREA:
        srr_semiheated = total_semiheated_skylight_area / total_semiheated_roof_area

    return {
        getattr(SCC, "EXTERIOR_RESIDENTIAL"): srr_res,
        getattr(SCC, "EXTERIOR_NON_RESIDENTIAL"): srr_nonres,
        getattr(SCC, "EXTERIOR_MIXED"): srr_mixed,
        getattr(SCC, "SEMI_EXTERIOR"): srr_semiheated,
    }


def _helper_calculate_skylight_area(surface: dict) -> Quantity:
    total_glazed_area = ZERO.AREA
    for subsurface in find_all("$.subsurfaces[*]", surface):
        glazed_area = getattr_(subsurface, "subsurface", "glazed_area")
        opaque_area = getattr_(subsurface, "subsurface", "opaque_area")
        if getattr_(subsurface, "subsurface", "classification") == DOOR:
            if glazed_area > opaque_area:
                total_glazed_area += glazed_area + opaque_area
        else:
            total_glazed_area += glazed_area + opaque_area
    return total_glazed_area
