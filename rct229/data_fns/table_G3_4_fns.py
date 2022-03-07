from rct229.data import data
from rct229.data_fns.table_utils import find_osstd_table_entry
from rct229.ruleset_functions.get_opaque_surface_type import (
    ABOVE_GRADE_WALL,
    BELOW_GRADE_WALL,
    FLOOR,
    HEATED_SOG,
    ROOF,
    UNHEATED_SOG,
)
from rct229.schema.config import ureg

# This dictionary maps the opaque surface types that are returned from get_opaque_surface_type()
# to the corresponding construction values in ashrae_90_1_prm_2019.construction_properties.json
SURFACE_TYPE_TO_CONSTRUCTION_MAP = {
    ABOVE_GRADE_WALL: "ExteriorWall",
    ROOF: "ExteriorRoof",
    HEATED_SOG: "GroundContactFloor",
    UNHEATED_SOG: "GroundContactFloor",
    FLOOR: "ExteriorFloor",
    BELOW_GRADE_WALL: "GroundContactWall",
}

# This dictionary maps surface conditioning categories as returned from get_surface_conditioning_category_dict()
# to the corresponding building category values in ashrae_90_1_prm_2019.construction_properties.json
SURFACE_CONDITIONING_CATEGORY_TO_BUILDING_CATEGORY_MAP = {
    "EXTERIOR RESIDENTIAL": "Residential",
    "EXTERIOR NON-RESIDENTIAL": "Nonresidential",
    "SEMI-EXTERIOR": "Semiheated",
}

# This dictionary maps the ClimateZone2019ASHRAE901 enumerations to
# the corresponding climate zone set values  in the OSSTD file ashrae_90_1_prm_2019.construction_properties.json
CLIMATE_ZONE_ENUMERATION_TO_CLIMATE_ZONE_SET_MAP = {
    "CZ0A": "ClimateZone 0",
    "CZ0B": "ClimateZone 0",
    "CZ1A": "ClimateZone 1",
    "CZ1B": "ClimateZone 1",
    "CZ2A": "ClimateZone 2",
    "CZ2B": "ClimateZone 2",
    "CZ3A": "ClimateZone 3",
    "CZ3B": "ClimateZone 3",
    "CZ3C": "ClimateZone 3",
    "CZ4A": "ClimateZone 4",
    "CZ4B": "ClimateZone 4",
    "CZ4C": "ClimateZone 4",
    "CZ5A": "ClimateZone 5",
    "CZ5B": "ClimateZone 5",
    "CZ5C": "ClimateZone 5",
    "CZ6A": "ClimateZone 6",
    "CZ6B": "ClimateZone 6",
    "CZ7": "ClimateZone 7",
    "CZ8": "ClimateZone 8",
}


# Helper function to add WWR to the search criteria for getting the correct
# Exterior windows, skylight and glass doors
def wwr_to_search_criteria(wwr, search_criteria):
    if wwr <= 10.0:
        search_criteria.append(("minimum_percent_of_surface", 0))
        search_criteria.append(("maximum_percent_of_surface", 10))
    elif wwr <= 20.0:
        search_criteria.append(("minimum_percent_of_surface", 10.1))
        search_criteria.append(("maximum_percent_of_surface", 20))
    elif wwr <= 30.0:
        search_criteria.append(("minimum_percent_of_surface", 20.1))
        search_criteria.append(("maximum_percent_of_surface", 30))
    elif wwr <= 40.0:
        search_criteria.append(("minimum_percent_of_surface", 30.1))
        search_criteria.append(("maximum_percent_of_surface", 40))
    else:
        search_criteria.append(("minimum_percent_of_surface", None))
        search_criteria.append(("maximum_percent_of_surface", None))


def table_G34_lookup(
    climate_zone, surface_conditioning_category, opaque_surface_type, wwr=None
):
    """Returns the assembly maxiumum values for a given climate zone, surface conditoning category
     and opaque sruface type as required by ASHRAE 90.1 Table G3.4-1 through G3.4-8

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZone2019ASHRAE901 enumeration values
    surface_conditioning_category : str
        A surface conditioning category as returned by get_surface_conditioning_category_dict()
    opaque_surface_type : str
        An opaque surface type as returned by get_opaque_surfact_type()
    wwr: float
        Window to wall ratio of the building, default to None, required for searching transparent
    Returns
    -------
    dict
        { assembly_maximum_u_value: Quantity - The assembly maximum u value given by Table G3.4-1 }

    """
    climate_zone_set = CLIMATE_ZONE_ENUMERATION_TO_CLIMATE_ZONE_SET_MAP[climate_zone]
    building_category = SURFACE_CONDITIONING_CATEGORY_TO_BUILDING_CATEGORY_MAP[
        surface_conditioning_category
    ]
    construction = SURFACE_TYPE_TO_CONSTRUCTION_MAP[opaque_surface_type]

    # TODO Need to revisit this code when space implementation is completed
    # construction_set = find_osstd_table_entry(
    #     [
    #         ("template", "90.1-PRM-2019"),
    #         ("building_type", "Any"),
    #         ("space_type", "Semiheated" if building_category == "Semiheated" else None),
    #         ("is_residential", "Yes" if building_category == "Residential" else "No")
    #     ],
    #     osstd_table=data["ashrae_90_1_prm_2019.construction_sets"]
    # )

    search_criteria = [
        ("climate_zone_set", climate_zone_set),
        ("intended_surface_type", construction),
        ("building_category", building_category),
    ]

    if wwr:
        wwr_to_search_criteria(wwr, search_criteria)

    osstd_entry = find_osstd_table_entry(
        search_criteria,
        osstd_table=data["ashrae_90_1_prm_2019.construction_properties"],
    )

    search_results = {}

    if osstd_entry["assembly_maximum_u_value"]:
        search_results["u_value"] = osstd_entry["assembly_maximum_u_value"] * (
            ureg.Btu_h / ureg.ft2 / ureg.delta_degF
        )
    if osstd_entry["assembly_maximum_f_factor"]:
        search_results["f_factor"] = osstd_entry["assembly_maximum_f_factor"] * (
            ureg.Btu_h / ureg.ft / ureg.delta_degF
        )
    if osstd_entry["assembly_maximum_c_factor"]:
        search_results["c_factor"] = osstd_entry["assembly_maximum_c_factor"] * (
            ureg.Btu_h / ureg.ft2 / ureg.delta_degF
        )
    # TODO need to add fenestration properties
    return search_results
