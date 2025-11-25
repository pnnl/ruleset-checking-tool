from rct229.rulesets.ashrae9012022.data import data
from rct229.rulesets.ashrae9012022.data_fns.table_utils import find_osstd_table_entry


def table_J_6_lookup(Set: str, output_variable: str) -> list[float]:
    """Returns the performance curve coefficients as specified in ASHRAE 90.1 Table J-6

    Parameters
    ----------
    Set : str
        One of the set specified in Table J-6 ("V", "X", "Y", "Z", "AA", "AB")
    output_variable: str
        One of the performance curve types ("EIR-f-T", "CAP-f-T", "EIR-f-PLR")

    Returns
    -------
    list of floats

    """

    if Set not in ("V", "X", "Y", "Z", "AA", "AB"):
        return None

    if output_variable not in ("EIR-f-T", "CAP-f-T", "EIR-f-PLR"):
        return None

    osstd_entry = find_osstd_table_entry(
        [("Set", Set)],
        osstd_table=data["ashrae_90_1_table_J_6"],
    )
    performance_coefficient = osstd_entry[output_variable]

    return performance_coefficient
