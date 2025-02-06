from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry


def table_g3_1_2_lookup(building_area_type: str) -> dict[str:str]:
    """

    Parameters
    ----------
    building_area_type: str
        building area type of the service water heating system (ServiceWaterHeatingSpaceOptions2019ASHRAE901)

    Returns
    -------
    baseline_heating_method: dict
        The `baseline_heating_method` value of the corresponding `building_area_type`
    """

    osstd_entry = find_osstd_table_entry(
        [("building_area_type", building_area_type)],
        osstd_table=data["ashrae_90_1_table_G3_1_1_2"],
    )

    baseline_heating_method = osstd_entry["baseline_heating_method"]

    return {"baseline_heating_method": baseline_heating_method}
