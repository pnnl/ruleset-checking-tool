from rct229.data import data
from rct229.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg

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

# minimum capacity and maximum capacity in the ashrae_90_1_table_3_5_3
minimum_capacity_threshold_list = [0, 150, 300]
maximum_capacity_threshold_list = [9999.99, 300, 150]


def table_G3_5_3_lookup(compressor_type, capacity):
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

    minimum_capacity = 0
    for min_threshold in minimum_capacity_threshold_list:
        if capacity > min_threshold:
            minimum_capacity = min_threshold

    maximum_capacity = maximum_capacity_threshold_list[0]
    for max_threshold in maximum_capacity_threshold_list:
        if capacity < max_threshold:
            maximum_capacity = max_threshold

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
        "minimum_full_load_efficiency_kw_per_ton": minimum_full_load_efficiency,
        "minimum_integrated_part_load_kw_per_ton": minimum_integrated_part_load,
    }
