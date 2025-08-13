from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

SpaceFunctionOptions = SchemaEnums.schema_enums["SpaceFunctionOptions"]
LightingSpaceOptions = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]


def get_building_lab_zones_list(rmd: dict) -> list[str]:
    """
    returns a list of all of the zones in the building that include a laboratory space

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema

    Returns
    -------
    a list of zone.ids for all zones that have a laboratory space in the building
    """
    laboratory_zone_list = []
    for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmd):
        if any(
            [
                space.get("function") == SpaceFunctionOptions.LABORATORY
                and space.get("lighting_space_type") is None
                or space.get("function") is None
                and space.get("lighting_space_type")
                == LightingSpaceOptions.LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM
                or space.get("function") == SpaceFunctionOptions.LABORATORY
                and LightingSpaceOptions.LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM
                for space in find_all("$.spaces[*]", zone)
            ]
        ):
            laboratory_zone_list.append(zone["id"])

    return laboratory_zone_list
