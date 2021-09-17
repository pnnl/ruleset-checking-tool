from rct229.data import data
from rct229.data.schema_enums import schema_enums
from rct229.utils.interp import strict_list_linear_interpolation

ElectricalPhase = schema_enums["ElectricalPhase"]
SINGLE_PHASE = ElectricalPhase.SINGLE_PHASE.name
THREE_PHASE = ElectricalPhase.THREE_PHASE.name
_table_8_4_4 = data["ashrae_90_1_prm_transformers"]

MIN_KVA = 15
MAX_SINGLE_PHASE_KVA = 333
MAX_THREE_PHASE_KVA = 1000


def table_8_4_4_in_range(phase, kVA):
    """
    Determines whether the capacity for a transformer is within the range of Table 8.4.4

    The capacity range of Table 8.4.4 is between 15kVA and 333kVA inclusive for single-phase transformers and
    between 15kVA and 1000kVA inclusive for three-phase transformers.

    Parameters
    -----------
    phase : str
        One of the ElectricalPhase enumeration values
    kVA : float
        The transformer capacity in kVA

    Returns
    --------
    bool
        True if the transformer capacity is in range and False otherwise

    """
    return kVA >= MIN_KVA and (
        (phase == SINGLE_PHASE and kVA <= MAX_SINGLE_PHASE_KVA)
        or (phase == THREE_PHASE and kVA <= MAX_THREE_PHASE_KVA)
    )


def table_8_4_4_lookup(phase, kVA):
    """Returns transformer efficiency required by ASHRAE 90.1 Table 8.4.4

    This function applies to low-voltage, dry-type distribution transformers
    with capacities >= 15KVA and
    <= 333kVA for single-phase or
    <= 1000kVA for three-phase.
    For capacities bewteen the listed values, linear interpolation is used.

    Parameters
    ----------
    phase : str
        One of the ElectricalPhase enumeration values
    kVA : float
        Transformer capacity in kVA

    Returns
    -------
    dict
        { efficiency: float – The required transformer efficiency as a decimal value }
    """
    # Check that the capacity is in range

    assert table_8_4_4_in_range(phase, kVA), "kVA out of range"

    # Create the lists to be used for linear interpolation
    table_lists = {
        SINGLE_PHASE: [
            (item["capacity"], item["efficiency"])
            for item in filter(
                lambda list_item: list_item["phase"] == "Single-Phase",
                _table_8_4_4["transformers"],
            )
        ],
        THREE_PHASE: [
            (item["capacity"], item["efficiency"])
            for item in filter(
                lambda list_item: list_item["phase"] == "Three-Phase",
                _table_8_4_4["transformers"],
            )
        ],
    }

    # Round to 4 figures to match Table 8.4.4.
    return {
        "efficiency": round(
            strict_list_linear_interpolation(table_lists[phase], kVA), 4
        )
    }
