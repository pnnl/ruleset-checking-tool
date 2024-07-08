from typing import TypedDict

from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry


class MechanicalEfficiency(TypedDict):
    mechanical_efficiency: float
    motor_type: str


def table_G3_9_2_lookup(number_of_stories: int) -> MechanicalEfficiency:
    """Returns the full-load motor efficiency for motors as required by ASHRAE 90.1 Table G3.9.2
    Parameters
    ----------
    number_of_stories: int
        number of stories including basement - the value must be greater than 0.

    Returns
    -------
    dict
        {mechanical_efficiency - The mechanical efficiency by Table G3.9.2
        motor_type - The motor type by Table G3.9.2}

    Raises:
    -------
        TypeError: when the number_of_stories is less or equal to 0, the function will raise this error
    """

    number_of_stories = (
        "less than or equal to 4" if number_of_stories <= 4 else "greater than 4"
    )

    ashrae_90_1_table_G3_9_2 = find_osstd_table_entry(
        [("number_of_stories", number_of_stories)],
        osstd_table=data["ashrae_90_1_table_G3_9_2"],
    )

    mechanical_efficiency = ashrae_90_1_table_G3_9_2["mechanical_efficiency"]
    motor_type = ashrae_90_1_table_G3_9_2["motor_type"]

    return {"mechanical_efficiency": mechanical_efficiency, "motor_type": motor_type}
