from rct229.rulesets.ashrae9012022.ruleset_functions.get_building_surface_conditioning_category_dict import (
    get_building_surface_conditioning_category_dict,
    SurfaceConditioningCategory,
)


def get_baseline_surface_conditioning_category_dict(
    climate_zone, building_b, constructions_b, building_p, constructions_p
):
    """Determines the surface conditioning category for every surface in the baseline building based on the requirement
    below.

    Space conditioning categories used to determine applicability of the envelope requirements in Tables G3.4-1 through
    G3.4-8 shall be the same as in the proposed design.
    Exception: Envelope components of the HVAC zones that are semiheated in the proposed design must meet conditioned
    envelope requirements in Tables G3.4-1 through G3.4-8 if, based on the sizing runs, these zones are served by a
    baseline system with sensible cooling output capacity >= 5 Btu/h·ft2 of floor area, or with heating output capacity
    greater than or equal to the criteria in Table G3.4-9, or that are indirectly conditioned spaces.

    Parameters
    ----------


    Returns
    -------
    dict
        A dictionary that maps surface IDs to one of the conditioning categories:
        EXTERIOR_RESIDENTIAL, EXTERIOR_NON_RESIDENTIAL, EXTERIOR_MIXED,
        SEMI_EXTERIOR, UNREGULATED
    """

    building_surface_conditioning_category_dict_b = (
        get_building_surface_conditioning_category_dict(
            climate_zone, building_b, constructions_b
        )
    )
    building_surface_conditioning_category_dict_p = (
        get_building_surface_conditioning_category_dict(
            climate_zone, building_p, constructions_p
        )
    )

    baseline_surface_conditioning_category_dict = {}
    for surface_id in building_surface_conditioning_category_dict_b:
        if (
            building_surface_conditioning_category_dict_p[surface_id]
            == SurfaceConditioningCategory.SEMI_EXTERIOR
        ):
            baseline_surface_conditioning_category_dict[
                surface_id
            ] = SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL
        else:
            baseline_surface_conditioning_category_dict[
                surface_id
            ] = building_surface_conditioning_category_dict_b[surface_id]

    return baseline_surface_conditioning_category_dict
