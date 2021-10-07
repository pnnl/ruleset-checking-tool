from rct229.data import data
from rct229.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg

# This dictionary maps the ExteriorLightingAreas2019ASHRAE901TableG36 enumerations to
# the corresponding lpd_space_type values in the file
# ashrae_90_1_table_G3_6.json

building_exterior_enumeration_to_lpd_space_type_map = {
    "UNCOVERED_PARKING_LOTS_AND_DRIVES": "Uncovered parking lots and drives",
    "WALKWAY_NARROW": "Walkway - narrow",
    "WALKWAY_WIDE": "Walkway - wide",
    "PLAZA_AREAS": "Plaza Areas",
    "SPECIAL_FEATURE_AREAS": "Special Feature Areas",
    "STAIRWAYS": "Stairways",
    "MAIN_ENTRANCE_DOOR": "Main entrance door",
    "OTHER_ENTRANCE_OR_EXIT_DOORS": "Other entrance or exit doors",
    "EXTERIOR_CANOPIES": "Exterior canopies",
    "OUTDOOR_SALES_OPEN_AREAS": "Outdoor sales - open areas",
    "STREET_FRONTAGE": "Street frontage",
    "NON_TRADABLE_FACADE": "Non-tradable facade",
    "BUILDING_FACADE":"Building facade",
    "AUTOMATED_TELLER_MACHINES":"Automated teller machines",
    "NIGHT_DEPOSITORIES":"Night depositories",
    "ENTRANCE_AND_GATEHOUSE":"Entrance and gatehouses",
    "EMERGENCY_VEHICLE_LOADING_AREA":"Emergency vehicle loading area",
    "DRIVE_UP_WINDOWS_FAST_FOOD":"Drive-up windows at fast-food restaurants",
    "PARKING_NEAR_24HR_RETAIL_ENTRANCES":"Parking near 24-hour retail entrances"
}

def table_G3_6_lookup(building_exterior_type_enum_val):
    """Returns the lighting power density for a building_exterior as
    required by ASHRAE 90.1 Table G3.6
    Parameters
    ----------
    building_exterior_type : str
        One of the ExteriorLightingAreas2019ASHRAE901TableG36 enumeration values

    Returns
    -------
    dict
        { lpd: Quantity - The lighting power density in watt per square foot given by Table G3.6,
        linear_lpd: Quantity - The lighting power density in watt per linear foot given by Table G3.6 }

    """
    building_exterior_type = building_exterior_enumeration_to_lpd_space_type_map[
        building_exterior_type_enum_val
    ]

    osstd_entry = find_osstd_table_entry(
        [("building_exterior_type", building_exterior_type)],
        osstd_table=data["ashrae_90_1_table_G3_6"],
    )

    watts_per_ft2 = osstd_entry["w/ft^2"]
    watts_per_linear_ft = osstd_entry["w/ft"]
    watt_per_location = osstd_entry["w/location"]
    lpd = watts_per_ft2 * ureg("watt / foot**2") if watts_per_ft2 is not None else None
    linear_lpd = watts_per_linear_ft * ureg("watt / foot") if watts_per_linear_ft is not None else None
    location_lpd = watt_per_location * ureg("watt") if watt_per_location is not None else None


    return {"lpd": lpd, "linear_lpd": linear_lpd, "location_lpd": location_lpd}