from pint import Quantity

from rct229.schema.config import ureg
from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entries
from rct229.utils.assertions import assert_


def table_7_8_lookup(
    equipment_type: str, input_power: Quantity, draw_pattern: str = ""
) -> list:
    """Returns the service water heater efficiency value(s) and metrics for a baseline service water heater as
    required by ASHRAE 90.1 Table 7.8

    Parameters
    ----------
    equipment_type : str
        One of "Electric storage water heater" or "Gas storage water heater"
    input_power : Quantity
        The input power of the service water heater, in kW for Electric and in Btu/h for Gas
    draw_pattern : str
        One of: "Very small", "Low", "Medium", "High", or "" if not applicable

    Returns
    -------
    list of dict
        [
            {
                "efficiency_value": 0.80,
                "efficiency_metric": "UNIFORM_EFFICIENCY_FACTOR",
            },
            {
                "efficiency_value": 0.05,
                "efficiency_metric": "STAND_BY_LOSS_FRACTION",
            },
        ]

    """
    # Validate equipment type
    valid_equipment_types = [
        "Electric storage water heater",
        "Gas storage water heater",
    ]
    assert (
        equipment_type in valid_equipment_types
    ), f"Invalid equipment type. Must be one of {valid_equipment_types}"

    # Validate draw pattern
    valid_draw_patterns = ["", "Very small", "Low", "Medium", "High"]
    assert (
        draw_pattern in valid_draw_patterns
    ), f"Invalid draw pattern. Must be one of {valid_draw_patterns}"

    # Filter entries by capacity thresholds
    capacity_matched = find_capacity_matched_entries(
        input_power, data["ashrae_90_1_table_7_8"]
    )

    # Build table filters based on equipment type and draw pattern
    filters = [("Equipment Type", equipment_type)]
    if draw_pattern:
        # Only add the draw pattern filter if it's specified (non-empty)
        filters.append(("Draw Pattern", draw_pattern))

    # Filter the entire table by equipment type (and draw pattern if provided)
    type_pattern_matched = find_osstd_table_entries(
        filters, osstd_table=data["ashrae_90_1_table_7_8"]
    )

    # Intersect the two filtered sets: only those that match capacity and type/pattern
    return [
        entry["Efficiency"]
        for entry in type_pattern_matched
        if entry in capacity_matched
    ]


def find_capacity_matched_entries(capacity: Quantity, data_table):
    """Return entries that match the given capacity based on their min/max thresholds and inclusivity.
    This function assumes 'capacity' is a Pint Quantity and that all table entries have units specified.
    """
    keys = list(data_table.keys())
    data_list = data_table[keys[0]]

    matched_entries = []
    for entry in data_list:
        min_data = entry.get("Capacity min")
        max_data = entry.get("Capacity max")

        # Check minimum capacity boundary if present
        if min_data is not None:
            min_val = min_data["value"] * ureg(min_data["unit"])
            min_inclusive = min_data.get("inclusive", True)
            if min_inclusive and capacity < min_val:
                continue
            if not min_inclusive and capacity <= min_val:
                continue

        # Check maximum capacity boundary if present
        if max_data is not None:
            max_val = max_data["value"] * ureg(max_data["unit"])
            max_inclusive = max_data.get("inclusive", True)
            if max_inclusive and capacity > max_val:
                continue
            if not max_inclusive and capacity >= max_val:
                continue

        # If we reach here, capacity meets both min and max requirements
        matched_entries.append(entry)

    return matched_entries
