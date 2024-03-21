from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg
from typing import TypedDict
from pint import Quantity


G3_5_3_TableSearchInfo = TypedDict(
    "G3_5_3_TableSearchInfo",
    {
        "minimum_full_load_efficiency": Quantity,
        "minimum_integrated_part_load": Quantity,
    },
)

# This dictionary maps the ChillerCompressorOptions enumerations to
# the corresponding chiller types
# ashrae_90_1_table_3_5_3.json
water_chiller_compressor_type_map = {
    "SCREW": "displacement",
    "CENTRIFUGAL": "centrifugal",
    "RECIPROCATING": "displacement",
    "SCROLL": "displacement",
    "POSITIVE_DISPLACEMENT": "displacement",
    "SINGLE_EFFECT_INDIRECT_FIRED_ABSORPTION": "displacement",
    "DOUBLE_EFFECT_INDIRECT_FIRED_ABSORPTION": "displacement",
    "SINGLE_EFFECT_DIRECT_FIRED_ABSORPTION": "displacement",
    "DOUBLE_EFFECT_DIRECT_FIRED_ABSORPTION": "displacement",
    "OTHER": "displacement",
}

# Make sure this line is a sorted (ascending order) list
capacity_threshold_list = [0, 150, 300, 9999.99]


def table_g3_5_3_lookup(
    compressor_type: str, capacity: float
) -> G3_5_3_TableSearchInfo:
    """Returns the chiller data based on compressor type and capacity
    required by ASHRAE 90.1 Table 3.2
    Parameters
    ----------
    compressor_type : str
        One of the ChillerCompressorOptions enumeration values
    capacity: quantity
        chiller rated capacity in Tons
    Returns
    -------
    dict
        { minimum_full_load_efficiency: Quantity - the minimum full load efficiency
          minimum_party_load_efficiency: Quantity - the minimum part load efficiency
        }
    """
    compressor_category = water_chiller_compressor_type_map[compressor_type]

    minimum_capacity = min(capacity_threshold_list)
    maximum_capacity = max(capacity_threshold_list)
    for capacity_threshold in capacity_threshold_list:
        if capacity >= capacity_threshold:
            minimum_capacity = capacity_threshold
        if capacity < capacity_threshold:
            maximum_capacity = capacity_threshold
            break

    osstd_entry = find_osstd_table_entry(
        [
            ("equipment_type", compressor_category),
            ("inclusive_minimum_capacity_tons", minimum_capacity),
            ("exclusive_maximum_capacity_tons", maximum_capacity),
        ],
        osstd_table=data["ashrae_90_1_table_G3_5_3"],
    )
    minimum_full_load_efficiency_val = osstd_entry[
        "minimum_full_load_efficiency_kw_per_ton"
    ]
    minimum_integrated_part_load_val = osstd_entry[
        "minimum_integrated_part_load_kw_per_ton"
    ]

    minimum_full_load_efficiency = minimum_full_load_efficiency_val * ureg(
        "kilowatt / ton"
    )
    minimum_integrated_part_load = minimum_integrated_part_load_val * ureg(
        "kilowatt / ton"
    )

    return {
        "minimum_full_load_efficiency": minimum_full_load_efficiency,
        "minimum_integrated_part_load": minimum_integrated_part_load,
    }
