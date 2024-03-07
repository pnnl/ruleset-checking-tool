import numpy as np

from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value

LEAP_YEAR_HRS = 8784
NON_LEAP_YEAR_HRS = 8760


def get_min_oa_cfm_sch_zone(rmi, zone_id, is_leap_year: bool = False):
    """Each zone can have multiple terminal units sering it in the proposed RMR and each of these units could supply OA CFM. In order to obtain a zone level OA CFM schedule the OA CFM provided by each terminal unit needs to be aggregated for each hour of the year. This function receives an RMR (B, U, or P) and a zone ID and loops through each terminal unit associated with the zone to create an aggregated 8760 for OA CFM for the zone.

    Parameters
    ----------
    rmi: json
        The RMR in which the OA CFM schedule will be determined for the specific Zone ID.
    zone_id:
        The Zone ID in which the aggregated (across the terminal units serving the zone) hourly OA CFM schedule will be determined.
    is_leap_year: bool, default: False
        Whether the year is a leap year or not.

    Returns
    -------
    list: An aggregated OA CFM hourly schedule for the zone (for each hour of the year, for each terminal unit, Terminal.minimum_outdoor_airflow is multiplied by Terminal.minimum_outdoor_airflow_multiplier_schedule, this product is summed across the terminal units for each hour of the year).
          None if the zone has no terminal or every terminal in the zone do not use minimum_outdoor_airflow_multiplier_schedule.
    """

    LEAP_YEAR_HRS = 8784
    NON_LEAP_YEAR_HRS = 8760
    year_hrs = LEAP_YEAR_HRS if is_leap_year else NON_LEAP_YEAR_HRS

    min_oa_cfm_sch_zone_array_list = []
    for terminal in find_all(
        f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id}")].terminals[*]',
        rmi,
    ):
        minimum_outdoor_airflow = getattr_(
            terminal, "terminal", "minimum_outdoor_airflow"
        )

        minimum_outdoor_airflow_multiplier_schedule_id = terminal.get(
            "minimum_outdoor_airflow_multiplier_schedule"
        )

        if minimum_outdoor_airflow_multiplier_schedule_id:
            minimum_outdoor_airflow_multiplier_schedule = getattr_(
                find_exactly_one_with_field_value(
                    "$.schedules[*]",
                    "id",
                    minimum_outdoor_airflow_multiplier_schedule_id,
                    rmi,
                ),
                "Schedule",
                "hourly_values",
            )

            assert_(
                year_hrs == len(minimum_outdoor_airflow_multiplier_schedule),
                f"The length of schedule has to be {year_hrs}, but is {len(minimum_outdoor_airflow_multiplier_schedule)}.",
            )
            min_oa_cfm_sch_zone_array = (
                np.array(minimum_outdoor_airflow_multiplier_schedule)
                * minimum_outdoor_airflow
            )
            min_oa_cfm_sch_zone_array_list.append(min_oa_cfm_sch_zone_array)

    if min_oa_cfm_sch_zone_array_list:
        if len(min_oa_cfm_sch_zone_array_list) == 1:
            # one schedule scenario
            min_OA_CFM_schedule_for_zones_array = min_oa_cfm_sch_zone_array_list[0]
        else:
            # multi-schedule scenario
            min_OA_CFM_schedule_for_zones_array = min_oa_cfm_sch_zone_array_list[0]
            for arr in min_oa_cfm_sch_zone_array_list[1:]:
                min_OA_CFM_schedule_for_zones_array += arr

        min_OA_CFM_schedule_for_zones = min_OA_CFM_schedule_for_zones_array.tolist()
    else:
        min_OA_CFM_schedule_for_zones = [0] * year_hrs

    return min_OA_CFM_schedule_for_zones
