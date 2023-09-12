from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg

# This dictionary maps the Space Type enumerations to
# the corresponding lpd values in ashrae_90_1_table_9_6_1.json

space_type_enumeration_to_lpd_map = {
    "GUEST_ROOM": "guest room",
    "DORMITORY_LIVING_QUARTERS": "dormitory - living quarters",
    "DWELLING_UNIT": "dwelling unit",
}


def table_9_6_1_lookup(space_type_enum_val):
    """Returns the lighting power density for a building or space type as
    required by ASHRAE 90.1 Table 9.6.1

    Parameters
    ----------
    space_type : str
        One of the BuildingType enumeration values
    Returns
    -------
    dict
        { lpd: Quantity - The lighting power density given by Table 9.6.1 [W/ft^2] }

    """
    space_type = space_type_enumeration_to_lpd_map[space_type_enum_val]
    osstd_entry = find_osstd_table_entry(
        [("space_type", space_type)],
        osstd_table=data["ashrae_90_1_table_9_6_1"],
    )
    watts_per_sqft = osstd_entry["w/ft^2"]
    lpd = watts_per_sqft * ureg("watt / foot**2")
    return {"lpd": lpd}
