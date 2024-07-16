from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_zone_likely_a_vestibule import (
    is_zone_likely_a_vestibule,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_zone_mechanically_heated_and_not_cooled import (
    is_zone_mechanically_heated_and_not_cooled,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_zone

LightingSpaceOptions2019ASHRAE901TG37 = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]

ELIGIBLE_SPACE_TYPES = [
    LightingSpaceOptions2019ASHRAE901TG37.STORAGE_ROOM_HOSPITAL,
    LightingSpaceOptions2019ASHRAE901TG37.STORAGE_ROOM_SMALL,
    LightingSpaceOptions2019ASHRAE901TG37.STORAGE_ROOM_LARGE,
    LightingSpaceOptions2019ASHRAE901TG37.WAREHOUSE_STORAGE_AREA_MEDIUM_TO_BULKY_PALLETIZED_ITEMS,
    LightingSpaceOptions2019ASHRAE901TG37.WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS,
    LightingSpaceOptions2019ASHRAE901TG37.STAIRWELL,
    LightingSpaceOptions2019ASHRAE901TG37.ELECTRICAL_MECHANICAL_ROOM,
    LightingSpaceOptions2019ASHRAE901TG37.RESTROOM_FACILITY_FOR_THE_VISUALLY_IMPAIRED,
    LightingSpaceOptions2019ASHRAE901TG37.RESTROOM_ALL_OTHERS,
]


def does_zone_meet_g3_1_1e(rmd_b: dict, rmd_p: dict, zone_id: str) -> bool:
    """
    determines whether a given zone meets the G3_1_1e exception "Thermal zones designed with heating-only systems in
    the proposed design serving storage rooms, stairwells, vestibules, electrical/mechanical rooms, and restrooms not
    exhausting or transferring air from mechanically cooled thermal zones in the proposed design shall use system
    type 9 or 10 in the baseline building design."

    Parameters
    ----------
    rmd_b dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema, baseline model
    rmd_p dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema, baseline model
    zone_id str
        zone id

    Returns
    -------

    """
    zone_b = find_exactly_one_zone(rmd_b, zone_id)

    zone_meet_g_3_1_1e = all(
        [
            space_b.get("lighting_space_type") in ELIGIBLE_SPACE_TYPES
            for space_b in find_all("$.spaces[*]", zone_b)
        ]
    )

    if not zone_meet_g_3_1_1e:
        zone_meet_g_3_1_1e = is_zone_likely_a_vestibule(rmd_b, zone_id)

    if zone_meet_g_3_1_1e:
        zone_meet_g_3_1_1e = is_zone_mechanically_heated_and_not_cooled(rmd_p, zone_id)

    return zone_meet_g_3_1_1e
