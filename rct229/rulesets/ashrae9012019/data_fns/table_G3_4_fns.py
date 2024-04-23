from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import assert_

# This dictionary maps the opaque surface types that are returned from get_opaque_surface_type()
# to the corresponding construction values in ashrae_90_1_prm_2019.construction_properties.json
SURFACE_TYPE_TO_CONSTRUCTION_MAP = {
    OST.ABOVE_GRADE_WALL: "ExteriorWall",
    OST.ROOF: "ExteriorRoof",
    OST.HEATED_SOG: "GroundContactFloor",
    OST.UNHEATED_SOG: "GroundContactFloor",
    OST.FLOOR: "ExteriorFloor",
    OST.BELOW_GRADE_WALL: "GroundContactWall",
    "VERTICAL GLAZING": "ExteriorWindow",
    "SKYLIGHT": "Skylight",
    "DOOR": "ExteriorDoor",
}

DOOR_SUBCLASSIFICATION_TYPE_TO_STANDARD_CONSTRUCTION_MAP = {
    "METAL_COILING_DOOR": "NonSwinging",
    "NONSWINGING_DOOR": "NonSwinging",
    "SECTIONAL_GARAGE_DOOR": "NonSwinging",
    "SWINGING_DOOR": "Swinging",
}

# This dictionary maps surface conditioning categories as returned from get_surface_conditioning_category_dict()
# to the corresponding building category values in ashrae_90_1_prm_2019.construction_properties.json
# TODO Temporary fix for EXTERIOR MIXED type surface -
#  Need to review with RDS on Surface_Conditioning_Category (Zone_Conditioning_Category) functions
SURFACE_CONDITIONING_CATEGORY_TO_BUILDING_CATEGORY_MAP = {
    "EXTERIOR RESIDENTIAL": "Residential",
    "EXTERIOR MIXED": "Nonresidential",
    "EXTERIOR NON-RESIDENTIAL": "Nonresidential",
    "SEMI-EXTERIOR": "Semiheated",
}

# This dictionary maps the ClimateZoneOptions2019ASHRAE901 enumerations to
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
def wwr_to_search_criteria(wwr):
    wwr_search_list = []
    if wwr <= 0.1:
        wwr_search_list.append(("minimum_percent_of_surface", 0))
        wwr_search_list.append(("maximum_percent_of_surface", 10))
    elif wwr <= 0.2:
        wwr_search_list.append(("minimum_percent_of_surface", 10.1))
        wwr_search_list.append(("maximum_percent_of_surface", 20))
    elif wwr <= 0.3:
        wwr_search_list.append(("minimum_percent_of_surface", 20.1))
        wwr_search_list.append(("maximum_percent_of_surface", 30))
    elif wwr <= 0.4:
        wwr_search_list.append(("minimum_percent_of_surface", 30.1))
        wwr_search_list.append(("maximum_percent_of_surface", 40))
    else:
        wwr_search_list.append(("minimum_percent_of_surface", None))
        wwr_search_list.append(("maximum_percent_of_surface", None))
    return wwr_search_list


# Helper function to add WWR to the search criteria for getting the correct
# Exterior skylight
def skylit_to_search_criteria(wwr):
    skylit_search_list = []
    if wwr <= 0.02:
        skylit_search_list.append(("minimum_percent_of_surface", 0))
        skylit_search_list.append(("maximum_percent_of_surface", 2.0))
    else:
        skylit_search_list.append(("minimum_percent_of_surface", 2.0))
        skylit_search_list.append(("maximum_percent_of_surface", None))
    return skylit_search_list


def table_G34_lookup(
    climate_zone,
    surface_conditioning_category,
    opaque_surface_type,
    wwr=None,
    skylit_wwr=None,
    classification=None,
):
    """Returns the assembly maximum values for a given climate zone, surface conditioning category
     and opaque surface type as required by ASHRAE 90.1 Table G3.4-1 through G3.4-8

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZoneOptions2019ASHRAE901 enumeration values
    surface_conditioning_category : str
        A surface conditioning category as returned by get_surface_conditioning_category_dict()
    opaque_surface_type : str
        An opaque surface type as returned by get_opaque_surfact_type()
    wwr: float
        Window to wall ratio of the building, default to None, required for searching transparent
    classification: string
        Used for specifying particular construction type from database
    Returns
    -------
    dict
        { assembly_maximum_u_value: Quantity - The assembly maximum u value given by Table G3.4-1 }

    """
    climate_zone_set = climate_zone_adjustment_for_fenestration_data(
        climate_zone,
        CLIMATE_ZONE_ENUMERATION_TO_CLIMATE_ZONE_SET_MAP[climate_zone],
        wwr or skylit_wwr,
    )
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

    assert_(
        wwr is None or skylit_wwr is None,
        "One of the `wwr` or `skylit_wwr` argument must be None.",
    )
    if wwr is not None:  # when `wwr == 0.0`, `if wwr:` becomes False
        search_criteria.extend(wwr_to_search_criteria(wwr))

    if skylit_wwr is not None:  # when `skylit_wwr ==0`, `if skylit_wwr:` becomes False
        search_criteria.extend(skylit_to_search_criteria(skylit_wwr))

    if classification is not None:
        search_criteria.append(
            (
                "standards_construction_type",
                DOOR_SUBCLASSIFICATION_TYPE_TO_STANDARD_CONSTRUCTION_MAP[
                    classification
                ],
            )
        )

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
    if osstd_entry["assembly_maximum_solar_heat_gain_coefficient"]:
        search_results["solar_heat_gain_coefficient"] = osstd_entry[
            "assembly_maximum_solar_heat_gain_coefficient"
        ]
    # TODO need to add fenestration properties
    return search_results


def climate_zone_adjustment_for_fenestration_data(
    rct_climate_zone: str, osstd_climate_zone: str, fenestration_request: bool
):
    """
    Helper function to adjust climate zone string:

    Parameters
    ----------
    rct_climate_zone
    osstd_climate_zone
    fenestration_request

    Returns
    -------

    """
    return (
        osstd_climate_zone + rct_climate_zone[-1]
        if fenestration_request and osstd_climate_zone.endswith("3")
        else osstd_climate_zone
    )
