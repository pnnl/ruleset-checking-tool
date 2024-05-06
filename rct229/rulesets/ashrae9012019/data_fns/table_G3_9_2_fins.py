from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry


def table_G3_9_2_lookup(number_of_stories: int) -> dict[str, float]:
    """Returns the full-load motor efficiency for motors as required by ASHRAE 90.1 Table G3.9.2
    Parameters
    ----------
    number_of_stories: int
        number of stories including basement

    Returns
    -------
    dict
        {mechanical_efficiency - The mechanical efficiency by Table G3.9.2}

    """

    number_of_stories = (
        "less than or equal to 4" if number_of_stories <= 4 else "greater than 4"
    )

    mechanical_efficiency = find_osstd_table_entry(
        [("number_of_stories", number_of_stories)],
        osstd_table=data["ashrae_90_1_table_G3_9_2"],
    )["mechanical_efficiency"]

    return {"mechanical_efficiency": mechanical_efficiency}
