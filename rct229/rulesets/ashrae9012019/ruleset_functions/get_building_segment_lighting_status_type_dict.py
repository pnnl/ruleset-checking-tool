from rct229.rulesets.ashrae9012019.data_fns.table_9_5_1_fns import table_9_5_1_lookup
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

NONE = SchemaEnums.schema_enums["LightingBuildingAreaOptions2019ASHRAE901T951TG38"].NONE


# Intended for export and internal use
class LightingStatusType:
    """Enumeration class for lighting status types"""

    NOT_YET_DESIGNED_OR_MATCH_TABLE_9_5_1: str = "NOT-YET DESIGNED OR MATCH TABLE_9_5_1"
    AS_DESIGNED_OR_AS_EXISTING: str = "AS-DESIGNED OR AS-EXISTING"


def get_building_segment_lighting_status_type_dict(
    building_segment: dict,
) -> dict[str, LightingStatusType]:
    """Returns a dictionary that maps building_segment id to a LightingStatusType

    Parameters
    ----------
    building_segment : dict
        A dictionary representing a building_segment as defined by the ASHRAE229 schema.

    Returns
    -------
    dict
        A dictionary of the form:
        {
            <building_segment id>: LightingStatusType
        }
    """
    lighting_building_area_type = building_segment.get("lighting_building_area_type")
    spaces = find_all("$.zones[*].spaces[*]", building_segment)

    # The return value dict
    building_segment_lighting_status_type_dict = {}

    if lighting_building_area_type is None or lighting_building_area_type == NONE:
        building_segment_lighting_status_type_dict = {
            space["id"]: LightingStatusType.AS_DESIGNED_OR_AS_EXISTING
            for space in spaces
        }
    else:
        allowable_lpd = table_9_5_1_lookup(lighting_building_area_type)["lpd"]
        for space in spaces:
            total_space_lpd = sum(
                find_all("interior_lighting[*].power_per_area", space)
            )
            building_segment_lighting_status_type_dict[space["id"]] = (
                LightingStatusType.NOT_YET_DESIGNED_OR_MATCH_TABLE_9_5_1
                if std_equal(total_space_lpd, allowable_lpd)
                else LightingStatusType.AS_DESIGNED_OR_AS_EXISTING
            )

    return building_segment_lighting_status_type_dict
