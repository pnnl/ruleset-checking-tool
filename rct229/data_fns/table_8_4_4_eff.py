from rct229.data import data
from rct229.data.schema_enums import schema_enums
from rct229.utils.interp import strict_list_linear_interpolation

ElectricalPhase = schema_enums["ElectricalPhase"]
SINGLE_PHASE = ElectricalPhase.SINGLE_PHASE.name
THREE_PHASE = ElectricalPhase.THREE_PHASE.name
_table_8_4_4 = data["table_8_4_4"]

MIN_KVA = 15
MAX_SINGLE_PHASE_KVA = 333
MAX_THREE_PHASE_KVA = 1000


def table_8_4_4_in_range(phase, kVA):
    return kVA >= MIN_KVA and (
        (phase == SINGLE_PHASE and kVA <= MAX_SINGLE_PHASE_KVA)
        or (phase == THREE_PHASE and kVA <= MAX_THREE_PHASE_KVA)
    )


def table_8_4_4_eff(phase, kVA):
    """Returns transformer efficiency required by ASHRAE 90.1 Table 8.4.4

    This function applies to low-voltage, dry-type distribution transformers
    with capacities >= 15KVA and
    <= 333kVA for single-phase or
    <= 1000kVA for three-phase.
    For capacities bewteen the listed values, linear interpolation is used.

    Parameters
    ----------
    type : TransformerType
        Enumerated transformer type
    kVA : float
        Transformer capacity in kVA

    Returns
    -------
    float
        The required transformer percentage efficiency
    """
    # Check that the capacity is in range
    if (
        kVA < MIN_KVA
        or (phase == SINGLE_PHASE and kVA > MAX_SINGLE_PHASE_KVA)
        or (phase == THREE_PHASE and kVA > MAX_THREE_PHASE_KVA)
    ):
        raise ValueError("kVA out of range")

    # Create the lists to be used for linear interpolation
    table_lists = {
        SINGLE_PHASE: [
            (item["kVA"], item["Efficiency"]) for item in _table_8_4_4[SINGLE_PHASE]
        ],
        THREE_PHASE: [
            (item["kVA"], item["Efficiency"]) for item in _table_8_4_4[THREE_PHASE]
        ],
    }

    return strict_list_linear_interpolation(table_lists[phase], kVA)
