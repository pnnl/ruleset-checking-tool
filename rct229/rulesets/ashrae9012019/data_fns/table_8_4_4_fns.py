from numpy import interp
from rct229.rulesets.ashrae9012019.data import data
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums

ElectricalPhase = SchemaEnums.schema_enums["ElectricalPhaseOptions"]
SINGLE_PHASE = ElectricalPhase.SINGLE_PHASE
THREE_PHASE = ElectricalPhase.THREE_PHASE
_table_8_4_4 = data["ashrae_90_1_prm_transformers"]

kVA = ureg("kilovolt * ampere")
MIN_CAPACITY = 15 * kVA
MAX_SINGLE_PHASE_CAPACITY = 333 * kVA
MAX_THREE_PHASE_CAPACITY = 1000 * kVA


def table_8_4_4_in_range(phase, capacity):
    """
    Determines whether the capacity for a transformer is within the range of Table 8.4.4

    The capacity range of Table 8.4.4 is between 15kVA and 333kVA inclusive for single-phase transformers and
    between 15kVA and 1000kVA inclusive for three-phase transformers.

    Parameters
    -----------
    phase : str
        One of the ElectricalPhase enumeration values
    capacity : Quantity
        The transformer capacity

    Returns
    --------
    bool
        True if the transformer capacity is in range and False otherwise

    """
    return capacity >= MIN_CAPACITY and (
        (phase == SINGLE_PHASE and capacity <= MAX_SINGLE_PHASE_CAPACITY)
        or (phase == THREE_PHASE and capacity <= MAX_THREE_PHASE_CAPACITY)
    )


def table_8_4_4_lookup(phase, capacity):
    """Returns transformer efficiency required by ASHRAE 90.1 Table 8.4.4

    This function applies to low-voltage, dry-type distribution transformers
    with capacities >= 15KVA and
    <= 333kVA for single-phase or
    <= 1000kVA for three-phase.
    For capacities between the listed values, linear interpolation is used.

    Parameters
    ----------
    phase : str
        One of the ElectricalPhase enumeration values
    capacity : Quantity
        Transformer capacity

    Returns
    -------
    dict
        { efficiency: float|NaN – The required transformer efficiency as a decimal value }
    """
    # Check that the capacity is in range

    assert table_8_4_4_in_range(phase, capacity), "capacity out of range"

    # Create the lists to be used for linear interpolation
    # NOTE: the capacities in the table are in kVA units
    single_phase_items = list(
        filter(
            lambda list_item: list_item["phase"] == "Single-Phase",
            _table_8_4_4["transformers"],
        )
    )
    three_phase_items = list(
        filter(
            lambda list_item: list_item["phase"] == "Three-Phase",
            _table_8_4_4["transformers"],
        )
    )
    table_lists = {
        SINGLE_PHASE: {
            "xp": [item["capacity"] for item in single_phase_items],
            "fp": [item["efficiency"] for item in single_phase_items],
        },
        THREE_PHASE: {
            "xp": [item["capacity"] for item in three_phase_items],
            "fp": [item["efficiency"] for item in three_phase_items],
        },
    }

    interp_val = interp(
        (capacity / ureg("kilovolt * ampere")).magnitude,
        table_lists[phase]["xp"],
        table_lists[phase]["fp"],
    )

    # Round to 4 figures to match Table 8.4.4.
    return {"efficiency": round(interp_val, 4)}
