from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg

# This dictionary maps the Lighting Space Type enumerations to
# the corresponding lpd values in ashrae_90_1_table_9_5_1.json

lighting_space_type_enumeration_to_lpd_map = {
    "AUTOMOTIVE_FACILITY": "Automotive facility",
    "CONVENTION_CENTER": "Convention center",
    "COURTHOUSE": "Courthouse",
    "DINING_BAR_LOUNGE_LEISURE": "Dining: Bar lounge/leisure",
    "DINING_CAFETERIA_FAST_FOOD": "Dining: Cafeteria/fast food",
    "DINING_FAMILY": "Dining: Family",
    "DORMITORY": "Dormitory",
    "EXERCISE_CENTER": "Exercise center",
    "FIRE_STATION": "Fire station",
    "GYMNASIUM": "Gymnasium",
    "HEALTH_CARE_CLINIC": "Health-care clinic",
    "HOSPITAL": "Hospital",
    "HOTEL_MOTEL": "Hotel/motel",
    "LIBRARY": "Library",
    "MANUFACTURING_FACILITY": "Manufacturing facility",
    "MOTION_PICTURE_THEATER": "Motion picture theater",
    "MULTIFAMILY": "Multifamily",
    "MUSEUM": "Museum",
    "OFFICE": "Office",
    "PARKING_GARAGE": "Parking garage",
    "PENITENTIARY": "Penitentiary",
    "PERFORMING_ARTS_THEATER": "Performing arts theater",
    "POLICE_STATION": "Police station",
    "POST_OFFICE": "Post office",
    "RELIGIOUS_FACILITY": "Religious facility",
    "RETAIL": "Retail",
    "SCHOOL_UNIVERSITY": "School/university",
    "SPORTS_ARENA": "Sports arena",
    "TOWN_HALL": "Town hall",
    "TRANSPORTATION": "Transportation",
    "WAREHOUSE": "Warehouse",
    "WORKSHOP": "Workshop",
}


def table_9_5_1_lookup(space_type_enum_val: str):
    """Returns the allowed lighting power density for a building area type as
    required by ASHRAE 90.1 Table 9.5.1

    Parameters
    ----------
    space_type : str
        One of the BuildingType enumeration values other than "NONE". The caller is
        responsible for handling the "NONE" case.

    Returns
    -------
    dict
        { lpd: Quantity - The lighting power density given by Table 9.6.1 [W/ft^2] }

    Raises
    ------
    AssertionError
        If called with space_type_enum_val set to "NONE"

    """
    # This table lookup does not handle the "NONE" LightingSpaceType enumerated value
    assert space_type_enum_val != "NONE"

    building_area_type = lighting_space_type_enumeration_to_lpd_map[space_type_enum_val]
    osstd_entry = find_osstd_table_entry(
        [("building_area_type", building_area_type)],
        osstd_table=data["ashrae_90_1_table_9_5_1"],
    )
    watts_per_sqft = osstd_entry["w/ft^2"]
    lpd = watts_per_sqft * ureg("watt / foot**2")

    return {"lpd": lpd}
