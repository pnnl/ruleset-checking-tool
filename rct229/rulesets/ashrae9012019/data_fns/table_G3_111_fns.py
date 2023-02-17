from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry

# This dictionary maps the VerticalFenestrationBuildingAreaOptions2019ASHRAE901 enumerations to
# the corresponding wwr_building_type in the OSSTD file
# ashrae_90_1_prm_2019.prm_wwr_bldg_type
VERTICAL_FENESTRATION_BUILDING_AREA_TYPE_TO_WWR_BUILDING_TYPE_MAP = {
    "GROCERY_STORE": "Grocery store",
    "HEALTHCARE_OUTPATIENT": "Healthcare (outpatient)",
    "HOSPITAL": "Hospital",
    "HOTEL_MOTEL_SMALL": "Hotel/motel <= 75 rooms",
    "HOTEL_MOTEL_LARGE": "Hotel/motel > 75 rooms",
    "OFFICE_SMALL": "Office <= 5,000 sq ft",
    "OFFICE_MEDIUM": "Office 5,000 to 50,000 sq ft",
    "OFFICE_LARGE": "Office > 50,000 sq ft",
    "RESTAURANT_QUICK_SERVICE": "Restaurant (quick service)",
    "RESTAURANT_FULL_SERVICE": "Restaurant (full service)",
    "RETAIL_STAND_ALONE": "Retail (stand alone)",
    "RETAIL_STRIP_MALL": "Retail (strip mall)",
    "SCHOOL_PRIMARY": "School (primary)",
    "SCHOOL_SECONDARY_AND_UNIVERSITY": "School (secondary and university)",
    "WAREHOUSE_NONREFRIGERATED": "Warehouse (nonrefrigerated)",
    "OTHER": "All others",
}


def table_G3_1_1_1_lookup(vertical_fenestration_building_area_type_enum_val):
    """Returns the baseline building vertical fenestration percentage for a building area type as
    required by ASHRAE 90.1 Table G3.1.1-1
    Parameters
    ----------
    vertical_fenestration_building_area_type_enum_val : str
        One of the VerticalFenestrationBuildingAreaOptions2019ASHRAE901 enumeration values
    Returns
    -------
    dict
        { wwr: float – The window to wall ratio given by Table G3.1.1-1 expressed as a decimal between 0 and 1 }

    """

    if vertical_fenestration_building_area_type_enum_val is None:
        return None

    wwr_building_type = (
        VERTICAL_FENESTRATION_BUILDING_AREA_TYPE_TO_WWR_BUILDING_TYPE_MAP[
            vertical_fenestration_building_area_type_enum_val
        ]
    )

    osstd_entry = find_osstd_table_entry(
        [("wwr_building_type", wwr_building_type)],
        osstd_table=data["ashrae_90_1_prm_2019.prm_wwr_bldg_type"],
    )
    wwr = osstd_entry["wwr"]

    return {"wwr": wwr}
